import os
import json
from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk
from dotenv import load_dotenv, find_dotenv # pip install python-dotenv
from datetime import datetime

aiPrompt = "You are a helpful scheduling assistant.\
 You cannot manipulate the schedule directly, only comment on it,\
and provide feedback relating to it. Keep your responses concise, with two sentences at most. If the user requests you to change something about the schedule,\
inform them you are not able to do so, and ask them to try entering \"command mode\". Likewise, if the user\
 requests something off-topic, please inform them that you are unable help them. \
 The current date and time is: \
" + str(datetime.today()) + ". A list of currently scheduled events is as follows:\n\
name:Fun Party, desc:Party at the bodega on 5th street, date:4/19/25, time:8pm\n\
name:Cool Party, desc:cocktail party with fancy dress code, date:4/21/25, time:10pm\n\
name:Hiking, desc:hiking in the appalachians, date:5/10/25, time:7am"

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
    if userInput == "STOP":
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