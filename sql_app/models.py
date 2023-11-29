from sqlalchemy import MetaData, Column, Boolean, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

metadata = MetaData()

class Book(Base):
    metadata
    __tablename__ = "Books"
    id = Column(Integer, primary_key = True)
    author = Column(String, nullable = True)
    year = Column(Integer, nullable = True)
    total_pages = Column(Integer, nullable = True)
    genre = Column(String, nullable = True)
    
