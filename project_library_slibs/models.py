from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    name = Column(String(100))
    avatar_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи: один пользователь → много книг / сообщений
    books = relationship("Book", back_populates="owner", cascade="all, delete-orphan")
    messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}')>"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    author = Column(String(150))
    link = Column(Text)
    added_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="books")

    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}')>"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' или 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="messages")

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, role='{self.role}')>"

if __name__ == "__main__":
    from database import engine, Base
    Base.metadata.create_all(bind=engine)
    print("✓ Таблицы созданы!")