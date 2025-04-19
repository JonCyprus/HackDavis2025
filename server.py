# Starts up the server and listens for requests

from flask import Flask, render_template, request
app = Flask(__name__)

# Homepage
@app.route('/', methods=['GET'])
def HomeEndpoint():
    if request.method == 'GET':
        return render_template('index.html')

##### Endpoints #####

## User endpoints
# All Users resource
@app.route('/users', methods=['GET'])
def GetUsersEndpoint():
    if request.method == 'GET':
        return GetAllUsers()
# Login
@app.route('/users/login', methods=['GET'])
def LoginEndpoint():
    if request.method == 'GET':
        return LoginUser()


# Listen and serve requests
if __name__ == '__main__':
    app.run(debug=True)