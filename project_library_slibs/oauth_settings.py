from flask import session, redirect, url_for, Blueprint
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv
from database import get_db
from crud import get_user_by_google_id, create_user

load_dotenv()
oauth_bp = Blueprint('oauth', __name__, url_prefix='/')
oauth = OAuth()
#
def init_oauth(app):
    oauth.init_app(app)

    google = oauth.register(
        name = 'google',
        client_id = os.getenv('GOOGLE_CLIENT_ID'),
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs = {'scope': 'openid profile email'}
    )

    @oauth_bp.route('/login')
    def login():
        redirect_uri = url_for('oauth.auth', _external=True)
        return google.authorize_redirect(redirect_uri)

    @oauth_bp.route('/auth/google/callback')
    def auth():
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        session['user'] = user_info
        google_id = user_info['sub']
        # 3. Открываем сессию БД на время этого запроса
        with next(get_db()) as db:
            existing_user = get_user_by_google_id(db, google_id)
            if not existing_user:
                user = create_user(db, google_id, user_info['email'], user_info['name'], user_info.get('picture'))
            else:
                user = existing_user
        session['user_id'] = user.id
        print("DB User ID:", session.get('user_id'))
        return redirect(url_for('main.index'))

    @oauth_bp.route('/logout')
    def logout():
        print("Выход из системы...")
        session.clear()
        session.modified = True
        return redirect(url_for('main.index'))

    return google