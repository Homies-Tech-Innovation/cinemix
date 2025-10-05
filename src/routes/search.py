from fastapi import APIRouter, Query, Request
from fastapi.responses import JSONResponse
from src.services.omdb_client import omdb_client
from src.utils import response_parser, logger, Endpoint
from src.models.response import ErrorResponse, ResponseStatus
from src.services.rate_limiter import rate_limiter
import time

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
async def search_movies(
    request: Request,
    title: str = Query(..., min_length=1, description="Movie title to search"),
    page: int = Query(1, ge=1, le=100, description="OMDb page number (1-100)"),
):
    """
    Search for movies by title using the OMDb API.

    - **title**: Required movie title
    - **page**: Optional page number (default: 1)
    """

    # --- Rate Limiting ---
    if not rate_limiter.allow_request():
        wait_time = rate_limiter.calculate_wait_time()
        client_ip = request.client.host if request.client else "unknown"
        logger.warning(f"Rate limit exceeded for {client_ip}, wait {wait_time:.2f}s")

        error_model = ErrorResponse(
            message="Too many requests. Please try again later.",
            error_code="RATE_LIMIT_EXCEEDED",
            status=ResponseStatus.ERROR,
            data={
                "retry_after_seconds": wait_time,
                "timestamp": time.time(),
            },
        )

        return JSONResponse(
            content=error_model.model_dump(),
            status_code=429,
            headers={"Retry-After": str(int(wait_time))},
        )

    try:
        # --- Call OMDb API properly with title & page params ---
        data, status_code = omdb_client.fetch_search(title=title, page=page)
        logger.info(f"OMDb search for '{title}' page={page}, status_code={status_code}")

        # --- Parse and map response ---
        response_model = response_parser.parse_response(
            data, status_code, Endpoint.SEARCH
        )
        http_status_code = (
            200 if response_model.status == ResponseStatus.SUCCESS else 400
        )

        return JSONResponse(
            content=response_model.model_dump(), status_code=http_status_code
        )

    except Exception as e:
        logger.error(f"Unexpected error in /search endpoint: {e}", exc_info=True)
        error_model = ErrorResponse(
            message="Internal server error",
            error_code="INTERNAL_ERROR",
            status=ResponseStatus.ERROR,
        )
        return JSONResponse(content=error_model.model_dump(), status_code=500)
