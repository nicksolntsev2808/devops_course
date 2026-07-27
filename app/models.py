from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, HttpUrl


class BookmarkCreate(BaseModel):
    url: HttpUrl
    title: str = Field(min_length=1, max_length=200)
    tags: list[str] = Field(default_factory=list)
    favorite: bool = False


class BookmarkUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    tags: Optional[list[str]] = None
    favorite: Optional[bool] = None


class BookmarkOut(BaseModel):
    id: str
    url: str
    title: str
    tags: list[str]
    favorite: bool
    created_at: datetime
    updated_at: datetime
