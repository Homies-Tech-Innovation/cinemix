import httpx
from src.config import settings
from functools import wraps


class OmdbClient:
    def __init__(self):
        self.timeout = httpx.Timeout(connect=5.0, read=10.0)
        self.client = httpx.Client(timeout=self.timeout)
        self.url = settings.OMDb_BASE_URL
        self.api_key = settings.OMDb_API_KEY

    @staticmethod
    def error_handler(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                return fn(*args, **kwargs)
            except httpx.RequestError as e:
                # Network-level errors
                return {"Response": "False", "Error": f"Request failed: {e}"}, 500
            except httpx.HTTPStatusError as e:
                # HTTP error
                return {
                    "Response": "False",
                    "Error": f"HTTP error: {e}",
                }, e.response.status_code

        return wrapper

    @error_handler
    def fetch_details(self, movie_id: str):
        """Fetch movie details by IMDb ID."""
        r = self.client.get(f"{self.url}/?i={movie_id}&apikey={self.api_key}")
        r.raise_for_status()
        return r.json(), r.status_code

    @error_handler
    def fetch_search(self, movie_title: str):
        """Search movie title."""
        r = self.client.get(f"{self.url}/?s={movie_title}&apikey={self.api_key}")
        r.raise_for_status()
        return r.json(), r.status_code


omdb_client = OmdbClient()
