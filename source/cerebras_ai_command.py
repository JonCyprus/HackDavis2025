import os
import json
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from dotenv import load_dotenv, find_dotenv # pip install python-dotenv
from datetime import datetime

# Find .env file, and pull the Cerebras API key. Attach a client.
load_dotenv(find_dotenv())
client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

# Format the task data storage
taskSchema = {
    "type": "object",
    "properties": {
        "command": {"type": "string"},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "date": {"type": "string"},
        "time": {"type": "string"},
    },
    "required": ["command", "title"],
    "additionalProperties": False
}

# Start a stream
aiPrompt = "You are a helpful planning assistant, scheduling tasks and goals at certain times. \
The current date (yyyy-mm-dd) and time (hh:mm:s.ms) is: " + str(datetime.today()) + ". \
Interpret the user input as a command to perform. \
The available commands are: \
ADD, REMOVE, EDIT. Fill parameters as needed. \
Here is a list of current tasks scheduled:\n\
Final Essay - 2025-04-19 - 21:00:00\n Awesome Party - 2025-05-20 - 16:00:00\n Fun Party - 2025-05-23 - 17:00:00"

completion = client.chat.completions.create(
    model="llama-4-scout-17b-16e-instruct",
    messages=[
        # Initial system prompt for the AI, and user prompt.
        {"role": "system", "content": aiPrompt},
        {"role": "user", "content": "schedule a hiking event in the appalachians on june 40th, 7am."}
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