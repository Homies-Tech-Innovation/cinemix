from fastapi import APIRouter
from src.utils import get_movie, get_search_data
from src.models import ResponseStatus
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/{query}")
def search_movies(query: str):
    response_model = get_search_data(query)
    http_status_code = 200 if response_model and response_model.status == ResponseStatus.SUCCESS else 400

    return JSONResponse(
        content=response_model.data, status_code=http_status_code
    )


@router.get("/id/{id}")
async def get_movie_details(id: str):
    response_model = await get_movie(id)
    http_status_code = 200 if response_model.status == ResponseStatus.SUCCESS else 400

    return JSONResponse(
        content=response_model.data, status_code=http_status_code
    )
