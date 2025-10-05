from src.config import settings
import time


class RateLimiter:
    """
    Implements a rate limiting mechanism, likely a variation of the
    Sliding Window Counter algorithm, using fixed-size time buckets.
    """

    def __init__(self):
        # Configuration settings for the rate limiter
        self.bucket_size = (
            settings.BUCKET_SIZE
        )  # Time duration for a single bucket (e.g., 1 second)
        self.max_threshold = (
            settings.MAX_THRESHOLD
        )  # Maximum allowed requests across the whole window
        self.window_size = (
            settings.WINDOW_SIZE
        )  # Total time duration of the sliding window (e.g., 60 seconds)

        # The window is an array of counters, where each element is a 'bucket'.
        # The length is the total window size divided by the bucket size.
        self.window = [0] * (self.window_size // self.bucket_size)

        # Pointer to the current active bucket in the window array
        self.pointer = 0

        # Timestamp of the last successful request check (used for calculating elapsed time)
        self.past_time = time.time()

    def allow_request(self):
        """
        Checks if the current request should be allowed based on the rate limit.
        Returns True if allowed, False otherwise.
        """
        current_time = time.time()
        elapsed = current_time - self.past_time

        # Calculate how many full time buckets have passed since the last check
        packets = int(elapsed // self.bucket_size)

        # Slide the window forward by 'packets' number of buckets.
        # This effectively 'forgets' the request counts in the buckets that
        # have just rotated out of the window.
        for _ in range(packets):
            # Move the pointer circularly (wrap around using modulo)
            self.pointer = (self.pointer + 1) % len(self.window)
            # Reset the count for the bucket the pointer has just moved into
            # (which is now the "current" bucket for time tracking)
            self.window[self.pointer] = 0

        # Update the last checked time to the current time, adjusted to the last full bucket end
        self.past_time = current_time

        # Increment the count for the current active bucket
        self.window[self.pointer] += 1

        # Check if the total request count in the window exceeds the maximum threshold
        if sum(self.window) > self.max_threshold:
            # If rate limited, decrement the count (rollback) and deny the request
            self.window[self.pointer] -= 1
            return False
        else:
            # Request is within the limit, allow it
            return True

    def calculate_wait_time(self):
        """
        Returns the number of seconds the client should wait before
        the next request is allowed.
        """
        total_requests = sum(self.window)

        if total_requests <= self.max_threshold:
            # If we're under the limit, the wait time is just the time until
            # the current partial bucket expires (i.e., time until the pointer moves).
            current_time = time.time()

            # This calculates how much time has passed since the start of the current bucket.
            time_since_last_bucket_start = (
                current_time - self.past_time
            ) % self.bucket_size

            # The remaining time until the current bucket expires/rotates.
            return self.bucket_size - time_since_last_bucket_start

        # Count how many requests need to "fall out" to allow a new request
        excess = total_requests - self.max_threshold + 1  # +1 for the next request

        # Sum buckets from the oldest to find when enough requests expire
        wait_time = 0
        index = (self.pointer + 1) % len(self.window)  # oldest bucket
        while excess > 0:
            excess -= self.window[index]
            wait_time += self.bucket_size
            index = (index + 1) % len(self.window)

        return wait_time


rate_limiter = RateLimiter()
