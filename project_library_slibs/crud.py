from sqlalchemy.orm import Session
from models import User, Book, ChatMessage
from datetime import datetime

# 1. Найти пользователя по Google ID
def get_user_by_google_id(session: Session, google_id: str) -> User | None:
    """Ищет пользователя по google_id"""
    return session.query(User).filter(User.google_id == google_id).first()

# 2. Создать нового пользователя
def create_user(session: Session, google_id: str, email: str, name: str, avatar_url: str = None) -> User:
    """Создает нового пользователя, возвращает объект"""
    new_user = User(google_id=google_id, email=email, name=name, avatar_url=avatar_url)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

# 3. Добавить книгу в библиотеку
def add_book(session: Session, user_id: int, title: str, author: str = None, link: str = None) -> Book:
    """Добавляет книгу пользователю"""
    new_book = Book(user_id=user_id, title=title, author=author, link=link)
    session.add(new_book)
    session.commit()
    session.refresh(new_book)
    return new_book

# 4. Получить все книги пользователя
def get_user_books(session: Session, user_id: int) -> list[Book]:
    """Возвращает все книги конкретного пользователя"""
    return session.query(Book).filter(Book.user_id == user_id).all()

# 5. Сохранить сообщение чата
def save_chat_message(session: Session, user_id: int, role: str, content: str) -> ChatMessage:
    """Сохраняет сообщение в историю чата"""
    msg = ChatMessage(user_id=user_id, role=role, content=content)
    session.add(msg)
    session.commit()
    session.refresh(msg)
    return msg