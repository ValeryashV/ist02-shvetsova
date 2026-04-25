from functools import wraps
from flask import session, redirect, url_for

#защита маршрутов
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            print("Доступ запрещён: пользователь не авторизован")
            return redirect(url_for('oauth.login'))
        return f(*args, **kwargs)
    return decorated_function