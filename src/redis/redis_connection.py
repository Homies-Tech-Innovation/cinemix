import redis.asyncio as redis
from src.config import settings
from src.utils import logger


class RedisClient:
    def __init__(self):
        # Redis client using env vars from src/config.py
        self.client = redis.from_url(
            str(settings.REDIS_URL),  # AnyUrl → str
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DB,
            decode_responses=True,  # ensures str, not bytes
        )

    async def check_connection(self):
        """Perform health check for Redis connection"""
        try:
            pong = await self.client.ping()
            if pong:
                logger.info("Redis connection established successfully")
            else:
                raise ConnectionError("Redis ping failed")
        except Exception as e:
            logger.error(f"Redis health failed: {e}")
            raise SystemExit(1)


# Singleton instance (shared across the app)
redis_client = RedisClient()
