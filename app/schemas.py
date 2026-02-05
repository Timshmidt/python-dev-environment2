# app/schemas.py
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime

# ========== Схемы для категорий ==========

class CategoryBase(BaseModel):
    """Базовая схема категории"""
    title: str = Field(..., min_length=1, max_length=100, 
                       description="Название категории")

class CategoryCreate(CategoryBase):
    """Схема для создания категории"""
    pass

class CategoryUpdate(CategoryBase):
    """Схема для обновления категории"""
    pass

class Category(CategoryBase):
    """Схема категории для ответа"""
    id: int
    books_count: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

# ========== Схемы для книг ==========

class BookBase(BaseModel):
    """Базовая схема книги"""
    title: str = Field(..., min_length=1, max_length=200, 
                       description="Название книги")
    description: Optional[str] = Field(None, max_length=2000, 
                                       description="Описание книги")
    price: float = Field(..., ge=0, description="Цена книги")
    url: Optional[str] = Field(None, max_length=500, 
                               description="Ссылка на книгу")
    category_id: int = Field(..., description="ID категории")

class BookCreate(BookBase):
    """Схема для создания книги"""
    pass

class BookUpdate(BookBase):
    """Схема для обновления книги"""
    pass

class Book(BookBase):
    """Схема книги для ответа"""
    id: int
    category: Optional[Category] = None
    
    model_config = ConfigDict(from_attributes=True)

# ========== Схемы для ответов API ==========

class HealthCheck(BaseModel):
    """Схема для проверки здоровья API"""
    status: str
    timestamp: datetime
    database: str

class ErrorResponse(BaseModel):
    """Схема для ошибок API"""
    detail: str
    error_code: Optional[str] = None