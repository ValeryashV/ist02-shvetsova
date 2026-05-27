from flask import Blueprint, Flask, render_template, request, session, redirect, url_for, jsonify
from project_library_slibs.auth import login_required  # Импортируем декоратор
import os
from dotenv import load_dotenv
from project_library_slibs.api_routes import open_library_client, google_books_client
from oauth_settings import init_oauth, oauth_bp
from mistral_client import get_ai_answer
from database import get_db, engine, Base
from models import User, Book, ChatMessage
from crud import (
    get_user_by_google_id, create_user,
    add_book, get_user_books,
    save_chat_message
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False

# Создаём таблицы в PostgreSQL при старте приложения
with app.app_context():
    Base.metadata.create_all(bind=engine)
    print("Таблицы PostgreSQL созданы/проверены")

init_oauth(app)
app.register_blueprint(oauth_bp)
main_bp = Blueprint('main', __name__)


@main_bp.route('/test-db')
def test_db_route():
    """Тестовый маршрут для проверки БД"""
    with next(get_db()) as db:
        # Пробуем найти тестового юзера
        user = get_user_by_google_id(db, "google_123")
        if user:
            books = get_user_books(db, user.id)
            return {
                "user": user.name,
                "books_count": len(books),
                "status": "БД работает!"
            }
        return jsonify({"status": "Пользователь не найден, но БД подключена"})

#Главная страница с формой, разветвление не/зарег
@main_bp.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')

#берем параметр url, разветвление
@main_bp.route('/dashboard')
@login_required
def dashboard():
    query = request.args.get('q', '')
    return render_template('dashboard.html', query=query)

#Обработка поиска
@main_bp.route('/find')
@login_required
def find_books():
    query = request.args.get('q', '')
    if not query:
        return "Введите тему проекта"
    try:
        open_library_books = open_library_client(query)
        google_books = google_books_client(query)
        books_data = {
            'open_library': open_library_books,
            'google_books': google_books
        }
        return render_template('results.html', books=books_data, query=query, show_search=True)
    except Exception as e:
        print(f"Ошибка: {e}")
        return f"Ошибка: {str(e)}", 500

@main_bp.route('/api/save-book', methods=['POST'])
@login_required
def save_book():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({"error": "Нужно указать название книги"}), 400
    # открываем серию бд
    with next(get_db()) as db:
        new_book = add_book(
            session=db,
            user_id=session['user_id'],
            title=data.get('title'),
            author=data.get('author'),
            link=data.get('link')
        )
    return jsonify({"success": True, "book_id": new_book.id}), 201

@main_bp.route('/api/get-books', methods=['GET'])
@login_required
def get_books():
    with next(get_db()) as db:
        books = get_user_books(db, session['user_id'])
        # Превращаем объекты SQLAlchemy в словари для JSON
        books_list = [{"id": b.id, "title": b.title, "author": b.author, "link": b.link} for b in books]
        return jsonify({"books": books_list})

#ai-помощник
@main_bp.route('/ask-ai',  methods=['GET', 'POST'])
@login_required
def ask_ai():
    chat_history = session.get('chat_history', [])
    if request.method == 'POST':
        user_question = request.form.get('question', '')
        answer, new_chat_history = get_ai_answer(user_question, chat_history)
        session['chat_history'] = new_chat_history
        return render_template('ask_ai.html', question=user_question, answer=answer, new_chat_history=new_chat_history)
    return render_template('ask_ai.html')


app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=False, port=5000)