from source.respondWithJSON import respondWithJSON
from . import prompting

def ChatPrompt(app, request):
    message = request.json.get('prompt')
    prompting.cerebrasChat(app, message)
    return 