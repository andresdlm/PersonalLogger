from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=1, max_length=150)
    overview: str = Field(min_length=1, max_length=1000)
    year: int = Field(ge=1900, le=2100)
    rating: float = Field(ge=1, le=10)