# Starts up the server and listens for requests
import json
from urllib.parse import quote_plus, urlencode

from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv


from flask import Flask, redirect, render_template, session, url_for, request
import os
from source.config import DevelopmentConfig, ProductionConfig

import source.handlers.auth as auth

# Load the .env file
envFile = find_dotenv()
if envFile:
    load_dotenv(envFile)

# Start up the application
app = Flask(__name__)

# Pick the config
env = os.getenv("FLASK_ENV", "development")
if env == "production":
    app.config.from_object(ProductionConfig)
else:
    app.config.from_object(DevelopmentConfig)

# Load in the .env variables
app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['CEREBRAS_API_KEY'] = os.getenv("CEREBRAS_API_KEY")
app.config['POSTGRES_URL'] = os.getenv("POSTGRES_URL")

# Setup the oauth for the app
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

app.config['0AUTH']=oauth

##### Endpoints #####
# Homepage
@app.route("/")
def home():
    return render_template("index.html", session=session.get('user'),
                           pretty=json.dumps(session.get('user'), indent=4))

## User endpoints
# All Users resource
@app.route('/users', methods=['GET'])
def GetUsersEndpoint():
    if request.method == 'GET':
        return GetAllUsers(app)
# Login
@app.route('/login', methods=['GET'])
def LoginEndpoint():
    if request.method == 'GET':
        return auth.LoginUser(app)

# Callback from login
@app.route("/callback", methods=['GET', "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.getenv("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )
# Listen and serve requests
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=os.getenv("PORT", 5000))