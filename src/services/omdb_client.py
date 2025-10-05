import httpx
from functools import wraps
from src.config import settings
from src.utils import logger


class OmdbClient:
    def __init__(self):
        self.timeout = httpx.Timeout(connect=5.0, read=10.0)
        self.client = httpx.Client(timeout=self.timeout)
        self.url = settings.OMDb_BASE_URL
        self.api_key = settings.OMDb_API_KEY

    @staticmethod
    def error_handler(fn):
        """Decorator to handle HTTP errors"""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except httpx.RequestError as e:
                logger.error(f"Request failed: {e}")
                return {"Response": "False", "Error": f"Request failed: {e}"}, 500
            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP status error: {e}")
                return {
                    "Response": "False",
                    "Error": f"HTTP error: {e.response.status_code}",
                }, e.response.status_code
            except Exception as e:
                logger.exception(f"Unexpected OMDb client error: {e}")
                return {"Response": "False", "Error": str(e)}, 500

        return wrapper

    @error_handler
    def fetch_details(self, movie_id: str):
        """Fetch movie details by IMDb ID."""
        logger.info(f"Fetching movie details for IMDb ID: {movie_id}")
        r = self.client.get(f"{self.url}/?i={movie_id}&apikey={self.api_key}")
        r.raise_for_status()
        return r.json(), r.status_code

    @error_handler
    def fetch_search(self, title: str, page: int = 1):
        """Search for movies by title (supports pagination)."""
        logger.info(f"Searching movies with title='{title}' page={page}")
        r = self.client.get(f"{self.url}/?s={title}&page={page}&apikey={self.api_key}")
        r.raise_for_status()
        return r.json(), r.status_code


# Singleton instance
omdb_client = OmdbClient()
