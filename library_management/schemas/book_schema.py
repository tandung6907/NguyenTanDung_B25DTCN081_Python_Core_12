from typing import Optional

from pydantic import BaseModel, ConfigDict

from library_management.schemas.author_schema import AuthorResponseSchema


class BookCreateSchema(BaseModel):
    title: str
    category: str
    price: float
    borrow_count: int = 0
    available_quantity: int = 0
    author_id: int


class BookUpdateSchema(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    borrow_count: Optional[int] = None
    available_quantity: Optional[int] = None
    author_id: Optional[int] = None


class BookResponseSchema(BaseModel):
    id: int
    title: str
    category: str
    price: float
    borrow_count: int
    available_quantity: int
    author_id: int
    author: AuthorResponseSchema

    model_config = ConfigDict(from_attributes=True)
