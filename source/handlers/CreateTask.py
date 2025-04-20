## Testing for task creation
from source.getEmail import getSessionEmail
from source.sql import createTask
from source.respondWithJSON import respondWithJSON

def CreateTask(app, request):
    email = getSessionEmail()
    data = request.get_json()

    createTask(email, data.get("title"), data.get("description"), data.get("time"))

    return respondWithJSON({})

"""
Expects a JSON payload request as
{
    "title": string
    "description": string
    "time": string of YYYY-MM-DD hour:min:sec
}
"""