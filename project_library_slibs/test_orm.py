from database import SessionLocal, engine, Base
from models import User, Book, ChatMessage
from crud import (
    get_user_by_google_id, create_user,
    add_book, get_user_books,
    save_chat_message
)

def main():
    # Создаём таблицы, если их нет (методичка рекомендует это здесь)
    Base.metadata.create_all(bind=engine)

    # Открываем сессию для работы с БД
    session = SessionLocal()

    try:
        print("Начинаем тестирование ORM...\n")

        # Создаём пользователя
        print("Создаём пользователя...")
        user = create_user(session, "google_123", "test@mail.ru", "Тестовый Юзер", "https://via.placeholder.com/40")
        print(f"Юзер: {user.name} (ID: {user.id})\n")

        # Добавляем книги
        print("Добавляем книги...")
        book1 = add_book(session, user.id, "Чистый код", "Роберт Мартин", "https://example.com/clean-code")
        book2 = add_book(session, user.id, "Совершенный код", "Стив Макконнелл", "https://example.com/completed-code")
        print(f"Добавлено: {book1.title}, {book2.title}\n")

        # Сохраняем сообщения чата
        print("Сохраняем историю чата...")
        save_chat_message(session, user.id, "user", "Привет, помоги с Python")
        save_chat_message(session, user.id, "assistant", "Конечно! Что именно нужно?")
        print("2 сообщения сохранены\n")

        # Читаем данные обратно
        print(" Проверяем чтение...")
        books = get_user_books(session, user.id)
        print(f"Книг у пользователя: {len(books)}")
        for b in books:
            print(f"  - {b.title} ({b.author})")

        # Поиск по google_id
        print("\n Ищем пользователя по google_id...")
        found = get_user_by_google_id(session, "google_123")
        if found:
            print(f"Найден: {found.email}")
        else:
            print("Не найден")

    except Exception as e:
        print(f" Ошибка: {e}")
        session.rollback()  # Откатываем транзакцию при ошибке
    finally:
        session.close()     # Обязательно закрываем сессию!
        print("\nТестирование завершено. Сессия закрыта.")

if __name__ == "__main__":
    main()