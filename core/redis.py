from redis.asyncio import Redis

from config.redis import RedisConfig

redis_client = Redis.from_url(
    RedisConfig.URL, password=RedisConfig.PASSWORD, decode_responses=True
)
