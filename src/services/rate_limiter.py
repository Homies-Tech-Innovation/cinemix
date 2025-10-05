# src/services/rate_limiter.py
import time
from src.utils import logger
from src.config import settings


class RateLimiter:
    """
    Sliding Window Counter Rate Limiter (for educational purposes).
    """

    def __init__(self):
        self.bucket_size = getattr(settings, "BUCKET_SIZE", 10)
        self.window_size = getattr(settings, "WINDOW_SIZE", 60)
        self.max_threshold = getattr(settings, "MAX_THRESHOLD", 10)

        self.num_buckets = self.window_size // self.bucket_size
        self.buckets = [0] * self.num_buckets
        self.current_index = 0
        self.last_update_time = time.time()

        logger.info(
            f"RateLimiter initialized: bucket_size={self.bucket_size}s, "
            f"window_size={self.window_size}s, threshold={self.max_threshold}"
        )

    def _advance_pointer(self):
        now = time.time()
        elapsed = now - self.last_update_time
        buckets_to_advance = int(elapsed // self.bucket_size)

        if buckets_to_advance > 0:
            for _ in range(min(buckets_to_advance, self.num_buckets)):
                self.current_index = (self.current_index + 1) % self.num_buckets
                self.buckets[self.current_index] = 0
            self.last_update_time = now

    def allow_request(self) -> bool:
        self._advance_pointer()

        total_requests = sum(self.buckets)
        if total_requests >= self.max_threshold:
            logger.warning(
                f"Rate limit exceeded: {total_requests}/{self.max_threshold} requests in window"
            )
            return False

        self.buckets[self.current_index] += 1
        logger.debug(
            f"Request allowed. Bucket[{self.current_index}]={self.buckets[self.current_index]}, "
            f"Total={total_requests + 1}/{self.max_threshold}"
        )
        return True


# Shared singleton instance
rate_limiter = RateLimiter()
