from fastapi import Depends, FastAPI, HTTPException

from typing import List

from sqlalchemy.orm import Session

import schema,crud,models

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/books/new", response_model=schema.Book)
def create_book(new: schema.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.get_by_id(db, id=new.id)
    if(db_book):
        raise HTTPException(status_code=400, detail=f"The book {db_book.title} was already added!")
    return crud.create_book(db=db, book=new)

@app.get("/books")
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db,skip=skip,limit=limit)
    return books
@app.get("/books/range", response_model=List[schema.Book])
def get_range(page: int = 1, db: Session = Depends(get_db)):
    books = crud.get_range(db,page,10)
    return books
@app.get("/books/info")
def get_info(db: Session = Depends(get_db)):
    all_books = crud.get_books(db,skip=0,limit=100)
    for id, book in enumerate(all_books):
       print(id, book.title)
@app.get("/books/next",response_model=List[schema.Book])
def next(page: int = 1, db: Session = Depends(get_db)):
    all_books = crud.get_books(db,skip=0,limit=100)
    if(page+1 > len(all_books)/10):
        return crud.get_range(db,page,10)
    else:
        return crud.get_range(db,page+1,10)
@app.get("/books/prev",response_model=List[schema.Book])
def prev(page: int = 1, db: Session = Depends(get_db)):
    all_books = crud.get_books(db,skip=0,limit=100)
    if(page-1 >= 1):
        return crud.get_range(db,page-1,10)
    else:
        return crud.get_range(db,page,10)


@app.get("/books/{id}", response_model=str)
def get_info(id: int, db: Session = Depends(get_db)):
    db_book = crud.get_by_id(db, id=id)
    if(db_book is None):
        raise HTTPException(status_code=404, detail="Not found")
    return db_book.title

@app.get("/books/{id}", response_model=schema.Book)
def get_about(id: int, db: Session = Depends(get_db)):
    db_book = crud.get_by_id(db, id=id)
    if(db_book is None):
        raise HTTPException(status_code=404, detail="Not found")
    return db_book