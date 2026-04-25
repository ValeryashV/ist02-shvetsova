from flask import session, redirect, url_for, Blueprint
from authlib.integrations.flask_client import OAuth
import os
from dotenv import load_dotenv

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
        return redirect(url_for('main.index'))

    @oauth_bp.route('/logout')
    def logout():
        print("Выход из системы...")
        session.clear()
        session.modified = True
        return redirect(url_for('main.index'))

    return google