# app/db/models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.db import Base

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False, unique=True)
    
    # Связь с книгами
    books = relationship("Book", back_populates="category", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    url = Column(String(500), default="")
    
    # Внешний ключ на категорию
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="CASCADE"))
    
    # Связь с категорией
    category = relationship("Category", back_populates="books")