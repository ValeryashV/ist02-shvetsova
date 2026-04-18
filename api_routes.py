import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

#API_client
def google_books_client(query):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {
        'q': query,
        'maxResults': 5,
    }
    headers = { 'User-Agent': 'Mozilla/5.0' }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        print(f'status code: {response.status_code}')

        if response.status_code == 200:
            return response.json()
        else:
            print(f'error response: {response.status_code}')
            return {
                'error': f'API вернул статус {response.status_code}',
                'details': response.text[:200]
            }
    except requests.exceptions.RequestException as e:
        print(f'error request: {e}')
        return {'error': 'Не удалось подключиться к API', 'details': str(e)}


def open_library_client(query):
    url = 'https://openlibrary.org/search.json'
    params = {
        'title': query,
        'limit': 5
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        print(f'Open Library Status: {response.status_code}')

        if response.status_code == 200:
            data = response.json()
            return {
                'total': data.get('numFound', 0),
                'books': data.get('docs', [])[:5],
            }
        else:
            return {'error': f'API вернул статус {response.status_code}'}
    except Exception as e:
        print(f'Open Library error: {e}')
        return {'error': 'Не удалось подключиться к Open Library', 'details': str(e)}

#API_routes
#google_books_api
@app.route('/search')
def search_books_route():
    query = request.args.get('q', 'Python programming')
    books_data = google_books_client(query)
    return jsonify(books_data)

#open_library_books_api
@app.route('/search_open')
def search_open_library_route():
    query = request.args.get('q', 'Python programming')
    books_data = open_library_client(query)
    return jsonify(books_data)


if __name__ == '__main__':
    print("\n" + "="*50)
    print("="*50)
    print("   Главная:        http://127.0.0.1:5000/")
    print("   Поиск (Google): http://127.0.0.1:5000/search")
    print("   Поиск (OpenLib):   http://127.0.0.1:5000/search_open")
    print("=" * 50 + "\n")
    app.run(debug=True, port=5000)