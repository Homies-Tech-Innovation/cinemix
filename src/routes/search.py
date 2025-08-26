from fastapi import APIRouter

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/")
def search_movies():
    return {"message": "search movie route"}


@router.get("/id/{id}")
def get_movie_details(id: int):
    return {"message": f"search movie with id {id}"}
