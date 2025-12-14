from fastapi import APIRouter
from src.utils import get_movie
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
def search_movies():
    return {"message": "search movie route"}


@router.get("/id/{id}")
async def get_movie_details(id: str):
    response_model = await get_movie(id)
    http_status_code = 200 if response_model.status == "success" else 400

    return JSONResponse(
        content=response_model.model_dump_json(), status_code=http_status_code
    )
