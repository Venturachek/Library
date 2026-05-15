from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.models.book import Genre


class AddBook(BaseModel):
    title: str
    author: str
    price: int
    genre: Genre


class Book(AddBook):
    id: int
    availability: bool
    available_from: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class PATCHBook(BaseModel):
    title: str | None = None
    author: str | None = None
    price: int | None = None
    genre: Genre | None = None

class AvailabilityBook(BaseModel):
    availability: bool
    available_from: datetime | None
