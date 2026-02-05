# app/main.py
from app.db.db import SessionLocal
from app.db.crud import get_categories, get_books, get_books_by_category

def main():
    """Основная функция для работы с базой данных"""
    print("=" * 60)
    print("БИБЛИОТЕКА КНИГ")
    print("=" * 60)
    
    # Создаем сессию
    db = SessionLocal()
    
    try:
        # Получаем все категории
        categories = get_categories(db)
        
        if not categories:
            print("В базе данных нет категорий.")
            print("Запустите 'python3 app/init_db.py' для инициализации.")
            return
        
        # Выводим категории
        print("\n📚 КАТЕГОРИИ КНИГ:")
        print("-" * 40)
        for category in categories:
            print(f"  {category.id}. {category.title}")
        
        # Получаем все книги с информацией о категориях
        books = get_books(db)
        
        print("\n📖 ВСЕ КНИГИ:")
        print("-" * 60)
        for book in books:
            print(f"  ID: {book.id}")
            print(f"  Название: {book.title}")
            print(f"  Категория: {book.category.title}")
            print(f"  Цена: {book.price:.2f} руб.")
            if book.description and len(book.description) > 100:
                print(f"  Описание: {book.description[:100]}...")
            elif book.description:
                print(f"  Описание: {book.description}")
            print(f"  Ссылка: {book.url if book.url else 'Нет ссылки'}")
            print("-" * 40)
        
        # Статистика
        print("\n📊 СТАТИСТИКА:")
        print("-" * 40)
        print(f"  Всего категорий: {len(categories)}")
        print(f"  Всего книг: {len(books)}")
        
        # Детальная статистика по категориям
        print("\n📈 КНИГ ПО КАТЕГОРИЯМ:")
        print("-" * 40)
        for category in categories:
            books_in_category = get_books_by_category(db, category.id)
            print(f"  {category.title}: {len(books_in_category)} книг")
        
        # Самая дорогая и дешевая книга
        if books:
            most_expensive = max(books, key=lambda x: x.price)
            cheapest = min(books, key=lambda x: x.price)
            print(f"\n💰 САМАЯ ДОРОГАЯ КНИГА: {most_expensive.title} ({most_expensive.price:.2f} руб.)")
            print(f"💸 САМАЯ ДЕШЕВАЯ КНИГА: {cheapest.title} ({cheapest.price:.2f} руб.)")
            
            # Средняя цена
            avg_price = sum(book.price for book in books) / len(books)
            print(f"📊 СРЕДНЯЯ ЦЕНА КНИГИ: {avg_price:.2f} руб.")
        
    except Exception as e:
        print(f"❌ Ошибка при работе с базой данных: {e}")
    finally:
        db.close()
        print("\n" + "=" * 60)
        print("Программа завершена.")

if __name__ == "__main__":
    main()