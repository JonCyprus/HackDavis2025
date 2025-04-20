from flask import Flask, send_from_directory, session
from authlib.integrations.flask_client import OAuth
from config import DevelopmentConfig
from handlers.auth import LoginUser, LoginCallback

app = Flask(__name__, static_folder='../public')

# Load configuration
app.config.from_object(DevelopmentConfig)

# Initialize OAuth
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    api_base_url=f"https://{app.config['AUTH0_DOMAIN']}",
    access_token_url=f"https://{app.config['AUTH0_DOMAIN']}/oauth/token",
    authorize_url=f"https://{app.config['AUTH0_DOMAIN']}/authorize",
    client_kwargs={
        'scope': 'openid profile email',
    },
)
app.config['0AUTH'] = oauth

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

# Auth routes
@app.route('/login')
def login():
    return LoginUser(app)

@app.route('/callback')
def callback():
    return LoginCallback(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
