from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from enum import Enum

class PetStatus(str, Enum):
    AVAILABLE = "available"
    PENDING = "pending"
    SOLD = "sold"

class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None

class Pet(BaseModel):
    id: Optional[int] = None
    name: str
    category: Optional[Category] = None
    photoUrls: Optional[List[str]] = None
    tags: Optional[List[Tag]] = None
    status: Optional[PetStatus] = None
