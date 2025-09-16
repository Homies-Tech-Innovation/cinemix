# src/models/search_responce.py
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import List
from src.models.movie_details import SearchResult  

# calling from movie_detail to prevent duplication
class SearchData(BaseModel):
    """
    Represents the search response payload from the Cinemix API.
    """
    search_results: List[SearchResult] = Field(
        ..., alias="Search", description="List of search results"
    )
    total_results: int = Field(
        ..., alias="totalResults", description="Total number of results"
    )

    # validate search results
    @field_validator("search_results", mode="after")
    def validate_results(cls, results: List[SearchResult]) -> List[SearchResult]:
        for r in results:
            if not r.title.strip():
                raise ValueError("SearchResult.title cannot be empty")
            if not r.id.strip():
                raise ValueError("SearchResult.id cannot be empty")
        return results

    # ensure total_results is always an int
    @field_validator("total_results", mode="before")
    def validate_total_results(cls, v):
        if isinstance(v, str) and v.isdigit():
            return int(v)
        if not isinstance(v, int):
            raise ValueError("total_results must be an integer")
        return v

    # model config
    model_config = ConfigDict(
        validate_by_name=True
    )
