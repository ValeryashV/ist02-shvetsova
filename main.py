from flask import Flask, render_template, request
from api_routes import open_library_client

app = Flask(__name__)


#Главная страница с формой
@app.route('/')
def home():
    return render_template('index.html')

#Обработка поиска
@app.route('/find')
def find_books():
    query = request.args.get('q', '')
    if not query:
        return "Введите тему проекта"
    books_data = open_library_client(query)
    return render_template('results.html', books=books_data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)