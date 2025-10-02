from src.models import MovieDetails
from typing import Optional
from src.redis import redis_client
from src.config import settings
import json


class CacheService:
    async def cache_movie(self, movie_id: str, movie_obj: MovieDetails) -> None:
        """
        Stores the movie details in Redis under the key `movie_[movie_id]`.
        TTL is set to 1 hour.
        """
        await redis_client.client.set(
            f"movie_{movie_id}",
            json.dumps(movie_obj.model_dump()),
            ex=settings.CACHE_TTL,
        )

    async def get_movie(self, movie_id: str) -> Optional[MovieDetails]:
        """
        Retrieves the cached movie details from Redis.
        Returns None if the key does not exist.
        """
        cache = await redis_client.client.get(f"movie_{movie_id}")

        if cache:
            try:
                return MovieDetails(**(json.loads(cache)))
            except json.JSONDecodeError:
                return None
        return None


cache_service = CacheService
