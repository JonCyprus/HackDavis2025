from flask import session

## This is to handle the annoying bit of sessions and getting the emailfrom the token


def getSessionEmail():
    token = session['user']
    email = token['userinfo']['email']
    return email