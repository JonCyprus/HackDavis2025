# Called in the "CHAT MODE" of TaskLand.
# app.config["CURRENT_CHAT"] should contain an array of JSON objects, defining the conversation.

def cerebrasChat(app):
    import os
    import json
    from cerebras.cloud.sdk import Cerebras # pip install --upgrade cerebras_cloud_sdk

    # ifndef "CURRENT CONVERSATION", initialize it.
    if app.config.get("CURRENT_CHAT") == None:
        app.config["CURRENT_CHAT"] = [{"role": "system", "content": "You are a helpful AI assistant."}]

    # Placeholder prompt, remove when linking with app client
    prompt = "Empty prompt."

    currentChat = app.config("CURRENT_CHAT")
    userInput = prompt

    # Find .env file, and pull the Cerebras API key. Attach a client.
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

    return aiResponse