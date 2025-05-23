# Starts up the server and listens for requests
import json
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv

from flask import Flask, redirect, render_template, session, url_for, request, send_from_directory, jsonify
import os
from source.config import DevelopmentConfig, ProductionConfig

import source.handlers as handlers

# Load the .env file
envFile = find_dotenv()
if envFile:
    load_dotenv(envFile)

# Start up the application
app = Flask(__name__, static_folder="templates/build/src", template_folder="templates/build")

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
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    fullPath = os.path.join("templates", "build", path)
    if path != "" and os.path.exists(fullPath):
        return send_from_directory(app.template_folder, path)
    return send_from_directory(app.template_folder, "index.html")
    
# Login
@app.route('/api/auth/login', methods=['GET'])
def LoginEndpoint():
    if request.method == 'GET':
        return handlers.LoginUser(app)

# Callback from login
@app.route("/callback", methods=['GET', "POST"])
def callback():
    return handlers.LoginCallback(app)

@app.route("/me")
def me():
    user = session.get("user")
    return jsonify({"user": user})


# Logout from user session
@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://" + os.getenv("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("/", _external=True), #ugh fix endpoint later
                "client_id": os.getenv("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

# Create a task endpoint
@app.route("/api/task", methods=["POST"])
def CreateTaskEndpoint():
    print("/api/task called.")
    return handlers.CreateTask(app, request)

# Send a prompt endpoint
@app.route("/api/prompt/chat", methods=["POST"])
def ChatPromptEndpoint():
   return handlers.ChatPrompt(app, request)

# auth status
@app.route('/api/auth/status')
def auth_status():
    return jsonify({
        'authenticated': 'user' in session,
        'user': session.get('user')
    })

# Return 
@app.route("/api/prompt/command", methods=["POST"])
def CommandPromptEndpoint():
    return handlers.CommandPrompt(app, request)

# Return current tasks in database
@app.route("/api/tasks", methods=["GET"])
def ReturnTasksEndpoint():
    return handlers.getAllTasks(app)

# Return tasks with sub-tasks
@app.route("/api/tasks/subtasks", methods=["GET"])
def ReturnSubtasksEndpoint():
    return handlers.getAllSubtasks(app)

# Listen and serve requests
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=os.getenv("PORT", 5000))

