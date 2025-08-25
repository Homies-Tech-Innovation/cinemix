### Redis Caching – Movie Details

We cache only the **Search by ID** results in Redis to reduce API calls to OMDb and improve response time.

**Caching Strategy:**

- Cache Key: `movie_[imdb_id]`
- TTL (Time-To-Live): 1 hour
- Stored Value: Serialized JSON of `MovieDetails` DTO

---

### Environment Variables

To connect to a cloud Redis instance, the following environment variables should be set:

```env
REDIS_URL=redis://<host>:<port>
REDIS_PASSWORD=<password>
REDIS_DB=<db_index>  # optional, default 0
CACHE_TTL=3600  # default 1 hour
```

---

### Function Signatures

```python
from pydantic import BaseModel
from typing import Optional

def cache_movie(movie_id: str, movie_obj: BaseModel) -> None:
    """
    Stores the movie details in Redis under the key `movie_[movie_id]`.
    TTL is set to 1 hour.
    """

def get_movie(movie_id: str) -> Optional[BaseModel]:
    """
    Retrieves the cached movie details from Redis.
    Returns None if the key does not exist.
    """
```

---

### Additional Setup Guidance

1. **Python Redis Client:**

   - Use the official `redis-py` package.
   - Example: `pip install redis`

2. **Connection Setup:**

   - Initialize Redis client with environment variables.
   - Always handle connection errors gracefully.

3. **Error Handling:**

   - If the Redis connection fails at app startup, log the error and exit the application.
   - This ensures the app does not run with missing caching infrastructure.

4. **Best Practices:**

   - Use a consistent key naming convention (`movie_[imdb_id]`).
   - Set TTL for all cached keys to avoid stale data.
   - Consider a monitoring solution to track cache hits/misses.
