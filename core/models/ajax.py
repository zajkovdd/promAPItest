
from pydantic import BaseModel, Field


class Response(BaseModel):
    success: bool
    error: str
    items: dict
    count: int
    title: str = Field(..., alias="title")