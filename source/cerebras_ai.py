import os
import json
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from dotenv import load_dotenv, find_dotenv # pip install python-dotenv

# Find .env file, and pull the Cerebras API key. Attach a client.
load_dotenv(find_dotenv())
client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

# Format the task data storage
taskSchema = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "start_time": {"type": "string"},
        "end_time": {"type": "string"},
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
        {"role": "user", "content": "Suggest something to do today between 4pm - 7pm"}
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