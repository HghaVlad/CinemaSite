from pydantic import BaseModel
from typing import Optional, List


class FilmResponse(BaseModel):
    id: int
    name: str
    genre: str
    duration: int
    age_restriction: str
    imdb_rating: Optional[float]
    description: Optional[str]
    poster_url: Optional[str]

    class Config:
        from_attributes = True


class FilmListResponse(BaseModel):
    films: List[FilmResponse]


class FilmCreate(BaseModel):
    name: str
    genre: str
    duration: int
    age_restriction: str
    imdb_rating: Optional[float]
    description: Optional[str]
    poster_url: Optional[str]