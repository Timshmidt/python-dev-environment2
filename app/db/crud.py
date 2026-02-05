# app/db/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from app.db import models
from . import models

# ========== CRUD для категорий ==========

def create_category(db: Session, title: str) -> models.Category:
    """Создание новой категории"""
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session, skip: int = 0, limit: int = 100) -> List[models.Category]:
    """Получение списка категорий"""
    return db.query(models.Category).offset(skip).limit(limit).all()

def get_category_by_id(db: Session, category_id: int) -> Optional[models.Category]:
    """Получение категории по ID"""
    return db.query(models.Category).filter(models.Category.id == category_id).first()

def update_category(db: Session, category_id: int, title: str) -> Optional[models.Category]:
    """Обновление категории"""
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db_category.title = title
        db.commit()
        db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int) -> bool:
    """Удаление категории"""
    db_category = get_category_by_id(db, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

# ========== CRUD для книг ==========

def create_book(
    db: Session, 
    title: str, 
    description: str, 
    price: float, 
    category_id: int,
    url: str = ""
) -> models.Book:
    """Создание новой книги"""
    db_book = models.Book(
        title=title,
        description=description,
        price=price,
        category_id=category_id,
        url=url
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100) -> List[models.Book]:
    """Получение списка книг с информацией о категории"""
    return db.query(models.Book).join(models.Category).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int) -> Optional[models.Book]:
    """Получение книги по ID"""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books_by_category(db: Session, category_id: int) -> List[models.Book]:
    """Получение книг по категории"""
    return db.query(models.Book).filter(models.Book.category_id == category_id).all()

def update_book(
    db: Session, 
    book_id: int, 
    title: str, 
    description: str, 
    price: float, 
    category_id: int,
    url: str = ""
) -> Optional[models.Book]:
    """Обновление книги"""
    db_book = get_book_by_id(db, book_id)
    if db_book:
        db_book.title = title
        db_book.description = description
        db_book.price = price
        db_book.category_id = category_id
        db_book.url = url
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int) -> bool:
    """Удаление книги"""
    db_book = get_book_by_id(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False

def get_categories_with_books(db: Session, skip: int = 0, limit: int = 100):
    """Получение категорий с книгами"""
    return db.query(models.Category).offset(skip).limit(limit).all()

def search_books(db: Session, title: Optional[str] = None, 
                 category_id: Optional[int] = None,
                 min_price: Optional[float] = None,
                 max_price: Optional[float] = None,
                 skip: int = 0, limit: int = 100):
    """Поиск книг по различным критериям"""
    query = db.query(models.Book).join(models.Category)
    
    if title:
        query = query.filter(models.Book.title.ilike(f"%{title}%"))
    if category_id:
        query = query.filter(models.Book.category_id == category_id)
    if min_price is not None:
        query = query.filter(models.Book.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Book.price <= max_price)
    
    return query.offset(skip).limit(limit).all()