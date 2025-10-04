from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel


class ResponseStatus(str, Enum):
    """
    Enum representing the status of a Cinemix API response.
    """

    SUCCESS = "success"
    ERROR = "error"


class Response(BaseModel):
    """
    Base response model for all Cinemix API responses.
    """

    message: str
    data: Optional[Dict[str, Any]] = None
    status: ResponseStatus


class ErrorResponse(Response):
    error_code: str
    data: Optional[Dict[str, Any]] = None
    status: ResponseStatus = ResponseStatus.ERROR
