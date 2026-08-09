from typing import List, Optional

from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from library_management.models.author_model import AuthorModel
from library_management.models.book_model import BookModel
from library_management.schemas.book_schema import BookCreateSchema, BookUpdateSchema


def get_all_books(db: Session) -> List[BookModel]:
    return db.query(BookModel).all()


def get_book_by_id(db: Session, book_id: int) -> Optional[BookModel]:
    return db.query(BookModel).filter(BookModel.id == book_id).first()


def create_book(db: Session, book_in: BookCreateSchema) -> BookModel:
    db_author = db.query(AuthorModel).filter(AuthorModel.id == book_in.author_id).first()
    if not db_author:
        raise HTTPException(
            status_code=400,
            detail=f"Mã tác giả author_id = {book_in.author_id} không tồn tại trong hệ thống CSDL!",
        )

    db_book = BookModel(**book_in.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book_in: BookUpdateSchema) -> Optional[BookModel]:
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        return None

    update_data = book_in.model_dump(exclude_unset=True)

    if "author_id" in update_data:
        db_author = db.query(AuthorModel).filter(AuthorModel.id == update_data["author_id"]).first()
        if not db_author:
            raise HTTPException(
                status_code=400,
                detail=f"Mã tác giả author_id = {update_data['author_id']} không tồn tại trong hệ thống CSDL!",
            )

    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int) -> bool:
    db_book = db.query(BookModel).filter(BookModel.id == book_id).first()
    if not db_book:
        return False

    db.delete(db_book)
    db.commit()
    return True


def search_books(db: Session, query: str) -> List[BookModel]:
    keyword = f"%{query}%"
    return db.query(BookModel).join(AuthorModel).filter(
        or_(
            BookModel.title.ilike(keyword),
            AuthorModel.name.ilike(keyword),
            BookModel.category.ilike(keyword),
        )
    ).all()


def get_borrow_warning_books(db: Session, threshold: int = 5) -> List[BookModel]:
    return db.query(BookModel).filter(BookModel.available_quantity <= threshold).all()


def get_top_borrowed_books(db: Session, limit: int = 5) -> List[BookModel]:
    return db.query(BookModel).order_by(BookModel.borrow_count.desc()).limit(limit).all()
