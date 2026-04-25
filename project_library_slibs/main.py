from flask import Blueprint, Flask, render_template, request, session, redirect, url_for
from project_library_slibs.auth import login_required  # Импортируем декоратор
import os
from dotenv import load_dotenv
from project_library_slibs.api_routes import open_library_client, google_books_client
from oauth_settings import init_oauth, oauth_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False


init_oauth(app)
app.register_blueprint(oauth_bp)
main_bp = Blueprint('main', __name__)



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


app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=False, port=5000)