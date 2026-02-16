import os
import asyncio
import logging
from typing import Callable, Optional
from livekit import rtc, api
from livekit.plugins import silero
from livekit.agents import vad
from google.adk.agents.live_request_queue import LiveRequestQueue
from google.genai import types

from ..core.interfaces import AudioProvider

logger = logging.getLogger(__name__)

class LiveKitAdapter(AudioProvider):
    def __init__(self):
        self._queue = LiveRequestQueue()
        self._room = rtc.Room()
        self._callback: Optional[Callable] = None
        # Gemini uses 24kHz usually
        self._audio_source = rtc.AudioSource(24000, 1)
        self._track = rtc.LocalAudioTrack.create_audio_track("agent_mic", self._audio_source)
        self._vad = silero.VAD.load()
        # Track active speakers for local audio gating
        self._active_speakers = 0

    async def start_session(self, room_id: str) -> None:
        url = os.getenv("LIVEKIT_URL")
        api_key = os.getenv("LIVEKIT_API_KEY")
        api_secret = os.getenv("LIVEKIT_API_SECRET")

        if not url or not api_key or not api_secret:
            logger.error("LiveKit credentials not found.")
            raise ValueError("LiveKit credentials not found")

        token = api.AccessToken(api_key, api_secret) \
            .with_identity("agent-host") \
            .with_name("Universal Host") \
            .with_grants(api.VideoGrants(room_join=True, room=room_id)) \
            .to_jwt()

        logger.info(f"Connecting to LiveKit room: {room_id}")

        @self._room.on("track_subscribed")
        def on_track_subscribed(track: rtc.Track, publication: rtc.RemoteTrackPublication, participant: rtc.RemoteParticipant):
            if track.kind == rtc.TrackKind.KIND_AUDIO:
                logger.info(f"Subscribed to audio track from {participant.identity}")
                # Create stream with 24kHz sample rate to match Gemini preference
                asyncio.create_task(self._handle_audio_stream(rtc.AudioStream(track, sample_rate=24000)))

        await self._room.connect(url, token)
        logger.info("Connected to LiveKit")

        await self._room.local_participant.publish_track(self._track)

    async def _handle_audio_stream(self, stream: rtc.AudioStream):
        # Local VAD stream for this track
        vad_stream = self._vad.stream()

        async def listen_vad():
            async for event in vad_stream:
                if event.type == vad.VADEventType.START_OF_SPEECH:
                    logger.info("VAD: Start of speech")

                    self._active_speakers += 1
                    # Signal ADK only on transition from 0 to 1 (first speaker)
                    if self._active_speakers == 1:
                        if hasattr(self._queue, "send_activity_start"):
                            self._queue.send_activity_start()

                    if self._callback:
                        if asyncio.iscoroutinefunction(self._callback):
                            await self._callback()
                        else:
                            self._callback()

                elif event.type == vad.VADEventType.END_OF_SPEECH:
                    logger.info("VAD: End of speech")

                    self._active_speakers = max(0, self._active_speakers - 1)
                    # Signal ADK only on transition to 0 (all silent)
                    if self._active_speakers == 0:
                        if hasattr(self._queue, "send_activity_end"):
                            self._queue.send_activity_end()

        # Start VAD listener
        asyncio.create_task(listen_vad())

        async for frame in stream:
            # Push to VAD
            vad_stream.push_frame(frame)

            # Push to Gemini
            # Data is int16 PCM at 24000Hz
            blob = types.Blob(
                mime_type="audio/pcm;rate=24000",
                data=frame.data.tobytes()
            )
            self._queue.send_realtime(blob)

    async def send_audio_chunk(self, chunk: bytes) -> None:
        # Local gating: drop audio if user is speaking
        if self._active_speakers > 0:
            return

        # chunk is PCM bytes
        # Create frame
        # Assuming 24kHz, mono, 16-bit
        samples_per_channel = len(chunk) // 2
        frame = rtc.AudioFrame(data=chunk, sample_rate=24000, num_channels=1, samples_per_channel=samples_per_channel)
        await self._audio_source.capture_frame(frame)

    async def on_user_speech(self, callback: Callable) -> None:
        self._callback = callback

    @property
    def live_request_queue(self) -> LiveRequestQueue:
        return self._queue
