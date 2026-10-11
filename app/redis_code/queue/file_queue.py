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

        try:
            message_id=await redis.xadd(
                self.STREAM_NAME,
                {
                    "file_id": file_id,
                    "bucket_name": bucket_name,
                    "user_id": user_id,
                    "mime_type": mime_type
                }
            )
            print("Redis stream:", self.STREAM_NAME)
            print("Redis message ID:", message_id)
        except Exception as e:
                    print("REDIS ERROR:", repr(e))
                    raise

file_queue = FileQueue()