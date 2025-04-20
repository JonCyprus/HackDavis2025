# This handles the authorization of the application
from flask import url_for, session, redirect
from source.sql import createUser

def LoginUser(app):
    return app.config['0AUTH'].auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )

def LoginCallback(app):
    oauth = app.config['0AUTH']
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    # Add the user to the SQL database
    userEmail = token['userinfo']['email']
    userPic = token['userinfo']['picture']
    createUser(userEmail, userPic)

    return redirect("/home")