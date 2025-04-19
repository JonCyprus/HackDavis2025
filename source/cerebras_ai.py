import os
import json
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from dotenv import load_dotenv, find_dotenv # pip install python-dotenv
from pathlib import Path

load_dotenv(find_dotenv())

client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

# Testing .env api retrieval
print(os.getenv("CEREBRAS_API_KEY"))