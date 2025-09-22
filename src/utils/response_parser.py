from src.models import MovieDetails, SearchData
from src.models import Response, ResponseStatus, ErrorResponse
from pydantic import ValidationError
from src.utils import logger
from enum import Enum


class Endpoint(Enum):
    SEARCH = "search"
    MOVIE_DETAILS = "details"


class ResponseParser:
    def parse_response(
        self, external_res, status_code: int, endpoint: Endpoint
    ) -> Response:
        """
        Parse the response from the upstream API (OMDb) and convert it into an internal Response.

        Handles both successful responses and error cases, including:
        - OMDb logical errors indicated by "Response": "False"
        - Invalid or unsupported endpoints
        - Validation errors when parsing into internal Pydantic models

        Args:
            external_res (dict): The JSON response from the API.
            status_code (int): The HTTP status code of the API response.
            endpoint (Endpoint): The endpoint that was called (e.g., SEARCH, MOVIE_DETAILS).

        Returns:
            Response: A Response object for success or an ErrorResponse for errors.
        """
        if external_res.get("Response") == "False":
            error_msg = external_res.get("Error", "Unknown error from upstream API")
            return ErrorResponse(
                error_code=str(status_code),
                message=error_msg,
                status=ResponseStatus.ERROR,
            )

        model_map = {Endpoint.MOVIE_DETAILS: MovieDetails, Endpoint.SEARCH: SearchData}

        model_cls = model_map.get(endpoint)

        if not model_cls:
            return ErrorResponse(
                error_code="400",
                message=f"Unsupported endpoint: {endpoint.value}",
                status=ResponseStatus.ERROR,
            )

        try:
            parsed_data: MovieDetails | SearchData = model_cls(**external_res)
            return Response(
                message="ok",
                data=parsed_data.model_dump(),
                status=ResponseStatus.SUCCESS,
            )
        except ValidationError as e:
            logger.error(f"Validation failed for {endpoint.value}: {e}")
            return ErrorResponse(
                error_code="422",
                message="Invalid response format from upstream API",
                status=ResponseStatus.ERROR,
            )


response_parser = ResponseParser()
