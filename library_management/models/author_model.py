from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from library_management.database import Base


class AuthorModel(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False)
    bio = Column(String(500), nullable=True)

    books = relationship("BookModel", back_populates="author")
