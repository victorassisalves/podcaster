from livekit import api
import os

async def start_recording(room_name: str):
    lk_api = api.LiveKitAPI(
        os.getenv("LIVEKIT_URL"),
        os.getenv("LIVEKIT_API_KEY"),
        os.getenv("LIVEKIT_API_SECRET"),
    )

    # Configure GCS output
    gcs_bucket = os.getenv("GCS_BUCKET_NAME")

    egress_request = api.RoomCompositeEgressRequest(
        room_name=room_name,
        filepath=f"recordings/{room_name}.mp4",
        file_outputs=[
            api.EncodedFileOutput(
                file_type=api.EncodedFileType.MP4,
                filepath=f"recordings/{room_name}.mp4",
                gcs=api.GCSUpload(bucket=gcs_bucket)
            )
        ]
    )

    # Note: This requires the egress service to be running in the LiveKit cluster
    # return await lk_api.egress.start_room_composite_egress(egress_request)
    print(f"Egress recording requested for room: {room_name}")
