import os
import json
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from dotenv import load_dotenv, find_dotenv # pip install python-dotenv

aiPrompt = "You are a helpful AI assistant, conversing with an end user."

# Find .env file, and pull the Cerebras API key. Attach a client.
load_dotenv(find_dotenv())
client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

currentChat = [
        {"role": "system", "content": aiPrompt}
    ]

# Input loop
while True:
    userInput = input()
    if userInput == "STOP!!!":
        break
    
    # Add user input to conversation history.
    currentChat.append({"role": "user", "content": userInput})

    # Start a stream
    chat = client.chat.completions.create(
        model="llama-4-scout-17b-16e-instruct",
        messages=currentChat
    )

    # Add AI response to conversation history, and print for the user.
    aiResponse = chat.choices[0].message.content
    print(aiResponse)
    currentChat.append({"role": "assistant", "content": aiResponse})
    
    # Loop