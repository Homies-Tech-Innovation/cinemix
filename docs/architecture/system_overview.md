# Cinemix Backend Overview

This document provides an overview of the Cinemix backend architecture, internal APIs, external API integration, caching, rate limiting, and logging strategies.

---

## 1. Backend API (Internal)

- **Base Path:** `/api/v1`
- **Future Versions:** `/api/v2` (breaking changes only)
- **Environments:**

  - Local: `http://localhost:8000/api/v1`
  - Production: `https://api.example.com/api/v1`

### Endpoints

1. **Search by Title** → `/api/v1/search/`
2. **Search by ID** → `/api/v1/search/id/`

Responses are standardized using **DTOs** with `snake_case` fields.

### Error Handling

FastAPI built-in error handler is customized:

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(HTTPException)
def http_exc_handler(req: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error_code": str(exc.status_code), "message": exc.detail}
    )
```

---

## 2. External API Integration – OMDb

- **Purpose:** Backend acts as a proxy layer to OMDb with caching, error handling, and rate limiting.
- **Endpoints:** `GET /api/?s=<query>&apikey=<api_key>` (search), `GET /api/?i=<id>&apikey=<api_key>` (details)
- **Error Handling:** Normalized JSON responses; frontend never sees raw OMDb errors.
- **Rate Limiting:** OMDb Free Tier: 1,000 requests per day.

---

## 3. Redis Caching – Movie Details

- **Cached Data:** Only **Search by ID** results.
- **Cache Key:** `movie_[imdb_id]`
- **TTL:** 1 hour
- **Stored Value:** JSON of `MovieDetails` DTO

**Environment Variables:**

```env
REDIS_URL=redis://<host>:<port>
REDIS_PASSWORD=<password>
REDIS_DB=<db_index>  # optional, default 0
CACHE_TTL=3600  # default 1 hour
```

**Function Signatures:**

```python
from pydantic import BaseModel
from typing import Optional

def cache_movie(movie_id: str, movie_obj: BaseModel) -> None:
    """Store MovieDetails in Redis with 1-hour TTL."""

def get_movie(movie_id: str) -> Optional[BaseModel]:
    """Retrieve MovieDetails from Redis or return None."""
```

**Setup Guidance:**

- Use `redis-py` (`pip install redis`)
- Initialize Redis client with environment variables
- Exit the app if Redis cannot connect at startup
- Use consistent key naming (`movie_[imdb_id]`)
- Monitor cache hits/misses (optional)

---

## 4. Rate Limiting (Learning Implementation)

- **Algorithm:** Sliding Window Counter (for educational purposes only)
- **Parameters:** Bucket Size = 10s, Window Size = 60s, Max Threshold = 10 requests per window
- **Environment Variables:**

```python
BUCKET_SIZE: int = 10
WINDOW_SIZE: int = 60
MAX_THRESHOLD: int = 10
```

- **Usage:**

```python
limiter = RateLimiter()
if limiter.allow_request():
    process_request()
else:
    reject_request()
```

---

## 5. Logger – Console-Based Logger

**Purpose:** Track API activity, cache usage, external requests, and errors during local development.

**Steps:**

1. **Initialize a Logger**

   - Use Python’s built-in `logging` module.
   - Set the default log level to `INFO` for normal operations.
   - Include timestamp, logger name, and log level in the format.

2. **Use Log Levels Appropriately**

   - **INFO** → Normal operations (API requests, cache hits, OMDb fetches).
   - **WARNING** → Recoverable issues (cache miss).
   - **ERROR** → Critical errors (Redis connection failure, unexpected exceptions).
   - **DEBUG** → Optional, for detailed internal debugging during development.

### Recommended Log Levels by Component

| Component                     | Log Level      | Notes                               |
| ----------------------------- | -------------- | ----------------------------------- |
| API requests & responses      | INFO           | Track normal usage                  |
| Redis cache hits/misses       | INFO / WARNING | INFO for hit, WARNING for miss      |
| External OMDb requests        | INFO           | Successful fetches                  |
| Errors (Redis/API/Unexpected) | ERROR          | Critical issues, should be reviewed |
| Debugging internal logic      | DEBUG          | Optional, use during development    |
