from app.core.redis_client import redis


class FileQueue:

    STREAM_NAME = "file_upload_queue"

    async def publish_file_uploaded(
        self,
        file_id: str,
        bucket_name: str,
        user_id: str,
        mime_type: str
    ):

        await redis.xadd(
            self.STREAM_NAME,
            {
                "file_id": file_id,
                "bucket_name": bucket_name,
                "user_id": user_id,
                "mime_type": mime_type
            }
        )


file_queue = FileQueue()