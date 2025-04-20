from source.respondWithJSON import respondWithJSON
from . import prompting # import from \source\handlers\prompting.py
import json

def ChatPrompt(app, request):
    print("Chat Prompt called, with params:")
    print(app)
    print(request)
    jsonReq = request.get_json()
    message = jsonReq.get("message")
    print("Calling cerebras Chat with message")
    print(message)
    response = prompting.cerebrasChat(app, message)
    return respondWithJSON({"response": response})