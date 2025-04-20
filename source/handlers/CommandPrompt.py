from source.respondWithJSON import respondWithJSON
from . import prompting # import from \source\handlers\prompting.py
import json

def CommandPrompt(app, request):
    print("Command Prompt called, with params:")
    print(app)
    print(request)
    jsonReq = request.get_json()
    message = jsonReq.get("message")
    print(message)
    resp = prompting.cerebrasCommand(app, message)
    return respondWithJSON({"response": resp})