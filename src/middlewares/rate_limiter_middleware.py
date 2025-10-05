from src.services import rate_limiter
from src.models import ErrorResponse
from fastapi import Request
from fastapi.responses import JSONResponse
import time


async def rate_limiter_middleware(request: Request, call_next):
    if not rate_limiter.allow_request():
        wait_time = rate_limiter.calculate_wait_time()

        error_model = ErrorResponse(
            message="Too many requests. Please try again later.",
            error_code="RATE_LIMIT_EXCEEDED",
            data={
                "retry_after_seconds": wait_time,
                "timestamp": time.time(),
            },
        )

        return JSONResponse(
            content=error_model.model_dump_json(),
            status_code=429,  # HTTP 429 Too Many Requests
            headers={"Retry-After": str(int(wait_time))},
        )

    return await call_next(request)
