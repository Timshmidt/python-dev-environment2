# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import sys
import os
from sqlalchemy import text

# Добавляем родительскую директорию в путь Python
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app.db.db import engine, Base
from app.api import books, categories
from app.schemas import HealthCheck

# Создаем таблицы (если их нет)
Base.metadata.create_all(bind=engine)

# Создаем приложение FastAPI
app = FastAPI(
    title="Bookstore API",
    description="API для управления книгами и категориями",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Настраиваем CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(categories.router)
app.include_router(books.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Корневой эндпоинт
    """
    return {
        "message": "Добро пожаловать в Bookstore API!",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthCheck, tags=["Health"])
def health_check():
    """
    Проверка состояния API и базы данных
    """
    try:
        # Проверяем подключение к БД
        with engine.connect() as conn:
            # Используем text() для SQL-запроса
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"disconnected: {str(e)}"
    
    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        database=db_status
    )

# Для запуска через python app/main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )