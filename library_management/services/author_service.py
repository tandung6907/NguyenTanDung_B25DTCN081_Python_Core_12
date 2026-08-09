from typing import List, Optional

from sqlalchemy.orm import Session

from library_management.models.author_model import AuthorModel
from library_management.schemas.author_schema import AuthorCreateSchema, AuthorUpdateSchema


def get_all_authors(db: Session) -> List[AuthorModel]:
    return db.query(AuthorModel).all()


def get_author_by_id(db: Session, author_id: int) -> Optional[AuthorModel]:
    return db.query(AuthorModel).filter(AuthorModel.id == author_id).first()


def create_author(db: Session, author_in: AuthorCreateSchema) -> AuthorModel:
    db_author = AuthorModel(**author_in.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def update_author(db: Session, author_id: int, author_in: AuthorUpdateSchema) -> Optional[AuthorModel]:
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not db_author:
        return None

    update_data = author_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_author, key, value)

    db.commit()
    db.refresh(db_author)
    return db_author


def delete_author(db: Session, author_id: int) -> bool:
    db_author = db.query(AuthorModel).filter(AuthorModel.id == author_id).first()
    if not db_author:
        return False

    db.delete(db_author)
    db.commit()
    return True
