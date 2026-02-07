"use client"
import {
  LiveKitRoom,
  VideoConference,
  RoomAudioRenderer,
  ControlBar,
} from '@livekit/components-react';
import '@livekit/components-styles';
import { useEffect, useState } from 'react';

export default function PodcastRoom({ params }: { params: { roomName: string } }) {
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    (async () => {
      const res = await fetch(`http://localhost:8000/api/token?room=${params.roomName}&identity=human-host`);
      const data = await res.json();
      setToken(data.token);
    })();
  }, [params.roomName]);

  if (!token) return <div className="p-24 text-center">Joining Room...</div>;

  return (
    <div className="h-screen bg-black">
      <LiveKitRoom
        video={false}
        audio={true}
        token={token}
        serverUrl={process.env.NEXT_PUBLIC_LIVEKIT_URL}
        data-lk-theme="default"
        style={{ height: '100dvh' }}
      >
        <VideoConference />
        <RoomAudioRenderer />
        <ControlBar />
      </LiveKitRoom>
    </div>
  );
}
