# app/api/categories.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db import crud, models
from app.db.db import get_db
from app.schemas import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[Category])
def read_categories(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Получить список категорий
    
    - **skip**: количество записей для пропуска (пагинация)
    - **limit**: максимальное количество возвращаемых записей
    """
    categories = crud.get_categories(db, skip=skip, limit=limit)
    
    # Добавляем количество книг в каждой категории
    for category in categories:
        category.books_count = len(category.books)
    
    return categories

@router.get("/{category_id}", response_model=Category)
def read_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить категорию по ID
    
    - **category_id**: ID категории
    """
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    
    # Добавляем количество книг
    db_category.books_count = len(db_category.books)
    
    return db_category

@router.post("/", 
             response_model=Category, 
             status_code=status.HTTP_201_CREATED)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db)
):
    """
    Создать новую категорию
    
    - **title**: название категории (обязательно)
    """
    # Проверяем, нет ли уже категории с таким названием
    existing_category = db.query(models.Category).filter(
        models.Category.title == category.title
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория с названием '{category.title}' уже существует"
        )
    
    return crud.create_category(db=db, title=category.title)

@router.put("/{category_id}", response_model=Category)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db)
):
    """
    Обновить категорию
    
    - **category_id**: ID категории для обновления
    - **title**: новое название категории
    """
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    
    # Проверяем, нет ли другой категории с таким названием
    existing_category = db.query(models.Category).filter(
        models.Category.title == category.title,
        models.Category.id != category_id
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Категория с названием '{category.title}' уже существует"
        )
    
    updated_category = crud.update_category(
        db=db, 
        category_id=category_id, 
        title=category.title
    )
    
    updated_category.books_count = len(updated_category.books)
    return updated_category

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db)
):
    """
    Удалить категорию
    
    - **category_id**: ID категории для удаления
    """
    db_category = crud.get_category_by_id(db, category_id=category_id)
    if db_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Категория с ID {category_id} не найдена"
        )
    
    # Проверяем, есть ли книги в категории
    if len(db_category.books) > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Нельзя удалить категорию, в которой есть книги. "
                   "Сначала удалите или переместите книги."
        )
    
    crud.delete_category(db=db, category_id=category_id)
    return None