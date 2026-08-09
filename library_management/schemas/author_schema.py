from typing import Optional

from pydantic import BaseModel, ConfigDict


class AuthorCreateSchema(BaseModel):
    name: str
    email: str
    bio: Optional[str] = None


class AuthorUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None


class AuthorResponseSchema(BaseModel):
    id: int
    name: str
    email: str

    model_config = ConfigDict(from_attributes=True)
