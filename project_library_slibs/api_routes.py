import requests
from flask import Flask, jsonify, request

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
            data = response.json()
            items = data.get('items', [])
            books = []
            for item in items:
                volume_info = item.get('volumeInfo', {})
                access_info = item.get('accessInfo', {})
                # Проверка на бесплатную книгу
                viewability = access_info.get('viewability', 'NO_PAGES')
                embeddable = access_info.get('embeddable', False)
                if viewability == 'NO_PAGES' and not embeddable:
                    continue
                if viewability not in ['ALL_PAGES', 'PARTIAL'] and not embeddable:
                    continue

                books.append({
                    'title': volume_info.get('title', 'Без названия'),
                    'authors': volume_info.get('authors', []),
                    'publishedDate': volume_info.get('publishedDate', ''),
                    'description': volume_info.get('description', ''),
                    'link': volume_info.get('infoLink', '#')
                })

            return books
        else:
            print(f'error response: {response.status_code}')
            return []

    except requests.exceptions.RequestException as e:
        print(f'error request: {e}')
        return []


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
            docs = data.get('docs', [])
            books = []
            for doc in docs[:5]:  # Берём первые 5
                books.append({
                    'title': doc.get('title', 'Без названия'),
                    'authors': doc.get('author_name', []),
                    'first_publish_year': doc.get('first_publish_year', ''),
                    'link': f"https://openlibrary.org{doc.get('key', '')}"
                })

            return books
        else:
            return []

    except Exception as e:
        print(f'Open Library error: {e}')
        return []
