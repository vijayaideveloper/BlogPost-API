
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CreatePost(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    published: bool = True


class PostResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
