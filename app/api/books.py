# app/api/books.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db import crud, models
from app.db.db import get_db
from app.schemas import Book, BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=List[Book])
def read_books(
    skip: int = 0,
    limit: int = 100,
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    title: Optional[str] = Query(None, description="Поиск по названию"),
    min_price: Optional[float] = Query(None, ge=0, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, ge=0, description="Максимальная цена"),
    db: Session = Depends(get_db)
):
    """
    Получить список книг
    
    - **skip**: количество записей для пропуска (пагинация)
    - **limit**: максимальное количество возвращаемых записей
    - **category_id**: фильтрация по категории
    - **title**: поиск по названию (регистронезависимый)
    - **min_price**: минимальная цена
    - **max_price**: максимальная цена
    """
    if any([title, category_id, min_price, max_price]):
        # Используем поиск с фильтрами
        books = crud.search_books(
            db=db,
            title=title,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=limit
        )
    else:
        # Просто получаем все книги
        books = crud.get_books(db, skip=skip, limit=limit)
    
    return books

@router.get("/{book_id}", response_model=Book)
def read_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить книгу по ID
    
    - **book_id**: ID книги
    """
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    return db_book

@router.post("/", 
             response_model=Book, 
             status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую книгу
    
    - **title**: название книги (обязательно)
    - **description**: описание книги
    - **price**: цена книги (обязательно)
    - **url**: ссылка на книгу
    - **category_id**: ID категории (обязательно)
    """
    # Проверяем существование категории
    db_category = crud.get_category_by_id(db, category_id=book.category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория с ID {book.category_id} не существует"
        )
    
    # Проверяем, нет ли уже книги с таким названием в этой категории
    existing_book = db.query(models.Book).filter(
        models.Book.title == book.title,
        models.Book.category_id == book.category_id
    ).first()
    
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Книга с названием '{book.title}' уже существует в этой категории"
        )
    
    return crud.create_book(
        db=db,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url
    )

@router.put("/{book_id}", response_model=Book)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить книгу
    
    - **book_id**: ID книги для обновления
    - **title**: новое название книги
    - **description**: новое описание книги
    - **price**: новая цена книги
    - **url**: новая ссылка на книгу
    - **category_id**: новая категория книги
    """
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    # Проверяем существование новой категории (если она меняется)
    if book.category_id != db_book.category_id:
        db_category = crud.get_category_by_id(db, category_id=book.category_id)
        if db_category is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Категория с ID {book.category_id} не существует"
            )
    
    # Проверяем, нет ли другой книги с таким названием в новой категории
    existing_book = db.query(models.Book).filter(
        models.Book.title == book.title,
        models.Book.category_id == book.category_id,
        models.Book.id != book_id
    ).first()
    
    if existing_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Книга с названием '{book.title}' уже существует в этой категории"
        )
    
    return crud.update_book(
        db=db,
        book_id=book_id,
        title=book.title,
        description=book.description,
        price=book.price,
        category_id=book.category_id,
        url=book.url
    )

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить книгу
    
    - **book_id**: ID книги для удаления
    """
    db_book = crud.get_book_by_id(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена"
        )
    
    crud.delete_book(db=db, book_id=book_id)
    return None