import sys
import os
sys.path.insert(0, os.getcwd())

from app.db.db import SessionLocal
from app.db.crud import create_category, create_book

db = SessionLocal()

try:
    # Создаем категории
    print("Создание категорий...")
    cat1 = create_category(db, "Программирование")
    cat2 = create_category(db, "Научная фантастика")
    cat3 = create_category(db, "Бизнес")
    
    # Создаем книги
    print("Создание книг...")
    create_book(db, "Python Cookbook", "Рецепты программирования на Python", 
                2000.00, cat1.id, "https://example.com/python-cookbook")
    create_book(db, "Django для профессионалов", "Полное руководство по Django", 
                2500.00, cat1.id, "https://example.com/django-pro")
    create_book(db, "Дюна", "Эпическая научная фантастика", 
                1500.00, cat2.id, "https://example.com/dune")
    create_book(db, "Основание", "Классика Азимова", 
                1200.00, cat2.id, "https://example.com/foundation")
    create_book(db, "Богатый папа, бедный папа", "Финансовая грамотность", 
                800.00, cat3.id, "https://example.com/rich-dad")
    
    print("✅ Тестовые данные созданы успешно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
finally:
    db.close()
	