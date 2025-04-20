# Starts up the server and listens for requests
import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

from flask import Flask, redirect, render_template, session, url_for, request, g, jsonify
import os
from source.config import DevelopmentConfig, ProductionConfig
from flask_cors import CORS  # You'll need to install this

import source.handlers as handlers
import source.sql.db as db

# Load the .env file
envFile = find_dotenv()
if envFile:
    load_dotenv(envFile)

# Start up the application
app = Flask(__name__)
CORS(app, supports_credentials=True)

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
    user = session.get('user')
    return render_template("index.html", session=user,
                           pretty=json.dumps(user, indent=4))

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
        return handlers.LoginUser(app)

# Callback from login
@app.route("/callback", methods=['GET', "POST"])
def callback():
    return handlers.LoginCallback(app)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.getenv("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("/", _external=True),
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# Create a task endpoint
@app.route("/test/createTask", methods=["POST"])
def CreateTaskEndpoint():
    return handlers.CreateTask(app, request)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    # Get tasks from database
    return jsonify(tasks)

@app.route('/api/tasks', methods=['POST'])
def create_task():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.json
    # Create task in database
    return jsonify(new_task)

@app.route('/api/chat', methods=['POST'])
def chat():
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    message = request.json.get('message')
    # Process with Cerebras AI
    return jsonify({'response': ai_response})

@app.route('/api/auth/status')
def auth_status():
    return jsonify({
        'authenticated': 'user' in session,
        'user': session.get('user')
    })

# Add this new endpoint
@app.route('/api/task', methods=['POST'])
def task_endpoint():
    # Pass the entire request object to the handler
    return handlers.handle_task_request(request)

# Listen and serve requests
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=os.getenv("PORT", 5000))

