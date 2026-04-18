from flask import Flask, session, redirect, url_for
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

load_dotenv()

app =Flask(__name__)
oauth = OAuth(app)
app.secret_key = os.getenv('SECRET_KEY')

google = oauth.register(
    name = 'google',
    client_id = os.getenv('GOOGLE_CLIENT_ID'),
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs = {'scope': 'openid profile email'}
)

@app.route('/')
def index():
    if 'user' in session:
        return f'{session["user"]['name']}, вы успешно вошли в Google <a href="/logout">Выход из аккаунта</a>'
    return '<a href="/login">Войти через Google</a>'

@app.route('/login')
def login():
    redirect_uri = url_for('auth', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def auth():
    token = google.authorize_access_token()
    user_info = token.get('userinfo')
    session['user'] = user_info
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug = True, port = 5000)