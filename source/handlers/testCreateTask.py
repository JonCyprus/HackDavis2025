## Testing for task creation
from flask import session


def testCreateTask(app):
    user = session['user']


