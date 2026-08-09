from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from library_management.database import get_db
from library_management.services import author_service
from library_management.schemas.author_schema import AuthorCreateSchema, AuthorResponseSchema, AuthorUpdateSchema

router = APIRouter(prefix="/api/v1/authors", tags=["Author Controller"])


@router.get("/", response_model=List[AuthorResponseSchema])
def get_authors(db: Session = Depends(get_db)):
    return author_service.get_all_authors(db)


@router.get("/{author_id}", response_model=AuthorResponseSchema)
def get_author(author_id: int, db: Session = Depends(get_db)):
    db_author = author_service.get_author_by_id(db, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Tác giả không tồn tại trong hệ thống")
    return db_author


@router.post("/", response_model=AuthorResponseSchema, status_code=201)
def add_author(author_in: AuthorCreateSchema, db: Session = Depends(get_db)):
    return author_service.create_author(db, author_in)


@router.put("/{author_id}", response_model=AuthorResponseSchema)
def edit_author(author_id: int, author_in: AuthorUpdateSchema, db: Session = Depends(get_db)):
    db_author = author_service.update_author(db, author_id, author_in)
    if not db_author:
        raise HTTPException(status_code=404, detail="Tác giả không tồn tại trong hệ thống")
    return db_author


@router.delete("/{author_id}")
def remove_author(author_id: int, db: Session = Depends(get_db)):
    deleted = author_service.delete_author(db, author_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tác giả không tồn tại trong hệ thống")
    return {"message": f"Đã xóa thành công tác giả ID {author_id}"}
