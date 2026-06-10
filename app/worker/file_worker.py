import asyncio

from app.core.redis_client import redis
from app.repositories.fs_node_query import FSNodeRepository
from app.db.session import AsyncSessionLocal


STREAM_NAME = "file_upload_queue"
GROUP_NAME = "file_workers"
CONSUMER_NAME = "worker-1"


async def create_group():
    print("GROUP CRETAE")
    try:
        await redis.xgroup_create( STREAM_NAME, GROUP_NAME, id="0", mkstream=True )
    except Exception:
        pass


async def process_message(data):
    file_id = data["file_id"]
    print("PROCESS MESSAGE")
    async with AsyncSessionLocal() as db:
        print("PROCESS MESSAGE 1")
        file_repo = FSNodeRepository(db)
        print("PROCESS MESSAGE 2")
        try:
            # mark processing
            await file_repo.chg_node_status(int(file_id), "PROCESSING")
            print("PROCESS MESSAGE 3")

            """
            your processing logic here

            Example:
            - verify file exists in R2
            - extract metadata
            - virus scan
            - generate thumbnail
            """

            # completed
            await file_repo.chg_node_status(int(file_id),"COMPLETED")

        except Exception as e:
            await file_repo.chg_node_status(int(file_id),"FAILED")
            print(e)
        finally:
            await db.close()


async def start_worker():
    print("START  WORKER")
    await create_group()
    while True:
        print("MESSAGE")
        messages = await redis.xreadgroup(
            groupname=GROUP_NAME,
            consumername=CONSUMER_NAME,
            streams={
                STREAM_NAME: ">"
            },
            count=10,
            block=5000
        )

        if not messages:
            continue

        for _, events in messages:
            for message_id, data in events:
                try:
                    print("STRART MESSGAE PROCESSING")
                    await process_message(data)
                    await redis.xack(STREAM_NAME, GROUP_NAME, message_id)
                except Exception as e:
                    print(e)


if __name__ == "__main__":

    asyncio.run(start_worker())