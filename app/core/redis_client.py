from redis.asyncio import Redis
#from redis import Redis
from app.core.config import setting

# redis = Redis.from_url(
#     "rediss://default:password@host:6379",
#     decode_responses=True
# )
url= setting.REDIS_URL
redis = Redis.from_url(
    url,
    decode_responses=True
)

# redis.set("test:name", "Ankit")

# # Read value
# value = redis.get("test:name")
