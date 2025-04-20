## Testing for task creation
from flask import session
from source.getEmail import getSessionEmail
from source.sql import createTask

def CreateTask(app, request):
    email = getSessionEmail()
    createTask(email, "hello", "testing", "2025-04-20 06:00:00,")
    return response

