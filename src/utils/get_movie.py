from src.services import cache_service, omdb_client
from src.models import MovieDetails
from src.utils import response_parser, Endpoint, logger


async def get_movie(movie_id: str):
    cache = await cache_service.get_movie(movie_id=movie_id)

    if not isinstance(cache, MovieDetails):
        data, status_code = omdb_client.fetch_details(movie_id=movie_id)
        
        if data.get("Response") != "False":
            movie = MovieDetails(**data)
            await cache_service.cache_movie(movie_id, movie)
            f"Cache miss for endpoint: {Endpoint.MOVIE_DETAILS}, caching movie id: {movie_id}"
        else:
            logger.error(
                f"OMDB API returned an error for movie id: {movie_id}, error: {data.get('Error')}"
            )
            
        return response_parser.parse_response(data, status_code, Endpoint.MOVIE_DETAILS)
    else:
        logger.info(
            f"Cache hit for endpoint: {Endpoint.MOVIE_DETAILS}, movie id: {movie_id}"
        )
        
    return response_parser.parse_response(
        cache.model_dump(by_alias=True), 200, Endpoint.MOVIE_DETAILS
    )
