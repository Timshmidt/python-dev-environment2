# app/init_db.py
import sys
import os

# Добавляем корень проекта в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.db import engine, Base
from app.db.crud import create_category, create_book
from app.db.db import SessionLocal

def init_database():
    """Инициализация базы данных"""
    print("Создание таблиц в базе данных...")
    
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)
    
    # Создаем сессию
    db = SessionLocal()
    
    try:
        # Проверяем, есть ли уже категории
        from app.db.crud import get_categories
        existing_categories = get_categories(db)
        
        if existing_categories:
            print("База данных уже инициализирована!")
            return
        
        print("Добавление тестовых данных...")
        
        # Создаем категории
        print("Создание категорий...")
        category1 = create_category(db, "Программирование")
        category2 = create_category(db, "Научная фантастика")
        category3 = create_category(db, "Бизнес и экономика")
        
        # Создаем книги для категории "Программирование"
        print("Добавление книг по программированию...")
        create_book(
            db,
            title="Чистый код: создание, анализ и рефакторинг",
            description="Руководство по написанию чистого кода от Роберта Мартина",
            price=2500.00,
            category_id=category1.id,
            url="https://example.com/clean-code"
        )
        
        create_book(
            db,
            title="Совершенный код",
            description="Полное руководство по разработке программного обеспечения",
            price=2200.00,
            category_id=category1.id,
            url="https://example.com/code-complete"
        )
        
        create_book(
            db,
            title="Python. Карманный справочник",
            description="Быстрый справочник по языку Python",
            price=800.00,
            category_id=category1.id,
            url="https://example.com/python-pocket"
        )
        
        # Создаем книги для категории "Научная фантастика"
        print("Добавление научно-фантастических книг...")
        create_book(
            db,
            title="Дюна",
            description="Эпическая научно-фантастическая сага Фрэнка Герберта",
            price=1500.00,
            category_id=category2.id,
            url="https://example.com/dune"
        )
        
        create_book(
            db,
            title="Основание",
            description="Классика научной фантастики Айзека Азимова",
            price=1200.00,
            category_id=category2.id,
            url="https://example.com/foundation"
        )
        
        # Создаем книги для категории "Бизнес и экономика"
        print("Добавление бизнес-литературы...")
        create_book(
            db,
            title="Богатый папа, бедный папа",
            description="Руководство по финансовой грамотности",
            price=900.00,
            category_id=category3.id,
            url="https://example.com/rich-dad"
        )
        
        create_book(
            db,
            title="Самый богатый человек в Вавилоне",
            description="Классика финансовой литературы",
            price=750.00,
            category_id=category3.id,
            url="https://example.com/babylon"
        )
        
        create_book(
            db,
            title="7 навыков высокоэффективных людей",
            description="Книга о личной и профессиональной эффективности",
            price=1300.00,
            category_id=category3.id,
            url="https://example.com/7-habits"
        )
        
        print("✅ База данных успешно инициализирована!")
        print(f"   Добавлено категорий: 3")
        print(f"   Добавлено книг: 7")
        
    except Exception as e:
        print(f"❌ Ошибка при инициализации базы данных: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()