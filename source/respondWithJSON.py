## Function to make it easier to respond with a JSON object
from flask import jsonify


def respondWithJSON(payload , status=200):
    return jsonify(payload), status