import os
import json
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from dotenv import load_dotenv, find_dotenv # pip install python-dotenv
from pathlib import Path

load_dotenv(find_dotenv())

client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

stream = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Why is an apple red? Explain in five sentences or less.",
        }
    ],
    model="llama-4-scout-17b-16e-instruct",
    stream=True,
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")