from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from library_management.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    borrow_count = Column(Integer, default=0)
    available_quantity = Column(Integer, default=0)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)

    author = relationship("AuthorModel", back_populates="books")
