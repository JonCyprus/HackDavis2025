import os
import json
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from datetime import datetime

# Helper function. Clears chat history. Sets CURRENT_CHAT to None.
def clearChatHistory(app):
    if app.config.get("CURRENT_CHAT") != None:
        app.config["CURRENT_CHAT"] = None

# Called in the "CHAT MODE" of TaskLand.
# app.config["CURRENT_CHAT"] should contain an array of JSON objects, defining the conversation.
def cerebrasChat(app):

    # FIXME: Access database for user information, and incorporate it into the AI system prompt.

    # ifndef "CURRENT CONVERSATION", initialize it.
    if app.config.get("CURRENT_CHAT") == None:
        aiPrompt = "You are a helpful AI assistant."
        app.config["CURRENT_CHAT"] = [{"role": "system", "content": aiPrompt}]

    # Placeholder prompt
    # FIXME: Access prompt data passed from front end.
    prompt = "Empty prompt."

    currentChat = app.config("CURRENT_CHAT")

    # Attach client to API key
    client = Cerebras(
        api_key=app.config["CEREBRAS_API_KEY"]
    )

    # Add user input to conversation history.
    currentChat.append({"role": "user", "content": prompt})

    # Start a stream
    chat = client.chat.completions.create(
        model="llama-4-scout-17b-16e-instruct",
        messages=currentChat
    )

    # Add AI response to conversation history, and print for the user.
    aiResponse = chat.choices[0]
    print(aiResponse)
    currentChat.append({"role": "assistant", "content": aiResponse})
    
    app.config["CURRENT_CHAT"] = currentChat

    return aiResponse

# Called in the "COMMAND MODE" of TaskLand
def cerebrasCommand(app):
    dateTime = datetime
    taskSchema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "dueDate": {"type": "string"},
    },
    "required": ["title", "start_time", "end_time"],
    "additionalProperties": False
    }

    # Start a stream
    completion = client.chat.completions.create(
        model="llama-4-scout-17b-16e-instruct",
        messages=[
            # Initial system prompt for the AI, and user prompt.
            {"role": "system", "content": "You are a helpful planning assistant, who manages activites for the day."},
            {"role": "user", "content": "Suggest something active to do today between 4pm - 7pm"}
        ],
        # Structure the response format
        response_format={
            "type": "json_schema", 
            "json_schema": {
                "name": "task_schema",
                "strict": True,
                "schema": taskSchema
            }
        }
    )

    # Print the JSON output to stdout
    taskSchema = json.loads(completion.choices[0].message.content)
    print(json.dumps(taskSchema, indent=2))