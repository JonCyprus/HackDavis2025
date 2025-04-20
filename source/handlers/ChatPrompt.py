from source.respondWithJSON import respondWithJSON
from . import prompting # import from \source\handlers\prompting.py
import json

def ChatPrompt(app, request):
    jsonReq = request.get_json()
    message = jsonReq.json.get("message")
    return json.jsonify({"response": prompting.cerebrasChat(app, message)}), 200