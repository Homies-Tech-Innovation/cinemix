from src.services import omdb_client
from src.utils import response_parser, Endpoint, logger

def get_search_data(query: str):
    data, status_code = omdb_client.fetch_search(movie_title=query)
    
    return response_parser.parse_response(data, status_code, Endpoint.SEARCH)
