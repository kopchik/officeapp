from typing import List

from pydantic import BaseModel, Field, HttpUrl


class SearchResult(BaseModel):
    """Schema to be used by integrations."""

    name: str
    size: int = Field(ge=0)
    url: HttpUrl
    owner: str


class SearchResults(BaseModel):
    __root__: List[SearchResult]
