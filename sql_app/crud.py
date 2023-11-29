from sqlalchemy import select
from sqlalchemy.orm import Session

import models, schema

# GET
def get_by_id(db: Session, id: int):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if book:
        return book
    else:
        return None
def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_range(db: Session, page: int = 1, size: int = 10):
    offset_min = page * size
    offset_max = (page + 1) * size
    books = db.query(models.Book).all()
    books_range = books[offset_min:offset_max]
    return books_range


# CREATE
def create_book(db: Session, book: schema.Book):
    db_books = models.Book(id=book.id, title=book.title, author=book.author,year=book.year,total_pages=book.total_pages,genre=book.genre)
    db.add(db_books)
    db.commit()
    db.refresh(db_books)
    return db_books