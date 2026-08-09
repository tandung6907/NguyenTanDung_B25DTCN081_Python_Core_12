from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from library_management.database import get_db
from library_management.services import book_service
from library_management.schemas.book_schema import BookCreateSchema, BookResponseSchema, BookUpdateSchema

router = APIRouter(prefix="/api/v1/books", tags=["Book Controller"])


@router.get("/search", response_model=List[BookResponseSchema])
def search_books(
    query: str = Query(..., description="Từ khóa tìm kiếm theo tiêu đề, tác giả hoặc thể loại"),
    db: Session = Depends(get_db),
):
    return book_service.search_books(db, query)


@router.get("/borrow-warning", response_model=List[BookResponseSchema])
def get_borrow_warning_books(
    threshold: int = Query(5, description="Ngưỡng số lượng sách khả dụng để cảnh báo"),
    db: Session = Depends(get_db),
):
    return book_service.get_borrow_warning_books(db, threshold)


@router.get("/top-borrowed", response_model=List[BookResponseSchema])
def get_top_borrowed_books(
    limit: int = Query(5, description="Số lượng sách được mượn nhiều nhất cần lấy"),
    db: Session = Depends(get_db),
):
    return book_service.get_top_borrowed_books(db, limit)


@router.get("/", response_model=List[BookResponseSchema])
def get_books(db: Session = Depends(get_db)):
    return book_service.get_all_books(db)


@router.get("/{book_id}", response_model=BookResponseSchema)
def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = book_service.get_book_by_id(db, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Sách không tồn tại trong hệ thống")
    return db_book


@router.post("/", response_model=BookResponseSchema, status_code=201)
def add_book(book_in: BookCreateSchema, db: Session = Depends(get_db)):
    return book_service.create_book(db, book_in)


@router.put("/{book_id}", response_model=BookResponseSchema)
def edit_book(book_id: int, book_in: BookUpdateSchema, db: Session = Depends(get_db)):
    db_book = book_service.update_book(db, book_id, book_in)
    if not db_book:
        raise HTTPException(status_code=404, detail="Sách không tồn tại trong hệ thống")
    return db_book


@router.delete("/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db)):
    deleted = book_service.delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sách không tồn tại trong hệ thống")
    return {"message": f"Đã xóa thành công sách ID {book_id}"}
