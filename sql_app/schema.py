from pydantic import BaseModel
class Book(BaseModel):
    id: int
    title: str
    author: str
    year: int
    total_pages: int
    genre: str
    class Config:
        from_attributes = True

class BookCreate(Book):
    pass