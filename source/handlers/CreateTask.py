## Testing for task creation
from source.getEmail import getSessionEmail
from source.sql import createTask
from source.respondWithJSON import respondWithJSON

def CreateTask(app, request):
    email = getSessionEmail()
    data = request.get_json()
    time = data.get("date") + " " + data.get("time")
    createTask(email, data.get("title"), data.get("description"), time)

    print("createTaskPassed.")
    return respondWithJSON({})

"""
Expects a JSON payload request as
{
    "title": string
    "description": string
    "time": string of YYYY-MM-DD hour:min:sec
}
"""