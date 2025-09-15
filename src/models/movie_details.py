from typing import List, Optional
from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    title: str = Field(..., alias="Title")
    year: str = Field(..., alias="Year")
    id: str = Field(..., alias="imdbID")
    type: str = Field(..., alias="Type")
    poster: Optional[str] = Field(None, alias="Poster")


class SearchData(BaseModel):
    search_results: List[SearchResult] = Field(..., alias="Search")
    total_results: str = Field(..., alias="totalResults")
    response: str = Field(..., alias="Response")


class MovieDetails(BaseModel):
    id: str = Field(..., alias="imdbID")
    title: str = Field(..., alias="Title")
    year: str = Field(..., alias="Year")
    type: str = Field(..., alias="Type")

    runtime: Optional[str] = Field(None, alias="Runtime")
    genre: Optional[str] = Field(None, alias="Genre")
    actors: Optional[str] = Field(None, alias="Actors")
    plot: Optional[str] = Field(None, alias="Plot")
    country: Optional[str] = Field(None, alias="Country")
    poster: Optional[str] = Field(None, alias="Poster")
    imdb_rating: Optional[str] = Field(None, alias="imdbRating")
    total_seasons: Optional[str] = Field(None, alias="totalSeasons")
