import logging

from flask import Flask, jsonify, request
import flask_cors
from google.appengine.ext import ndb
import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine

from google.appengine.ext import ndb

requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)

# Datastore Models
class Food(ndb.Model):
    friendly_id = ndb.StringProperty()
    message = ndb.TextProperty()
    food = ndb.TextProperty()
    calories = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

def query_database(user_id):
    ancestor_key = ndb.Key(Food, user_id)
    query = Food.query(ancestor=ancestor_key).order(-Food.created)
    food = query.fetch()
    
    list_of_food = []

    for f in food:
        list_of_food.append({
            'friendly_id': f.friendly_id,
            'message': f.message,
            'food': f.food,
            'calories': f.calories,
            'created': f.created
        })

    return list_of_food

@app.route('/food', methods=['GET'])
def list_food():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims: return 'Unauthorized', 401

    food = query_database(claims['sub'])
    return jsonify(food)

@app.route('/add_food', methods=['POST', 'PUT'])
def add_food():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims: return 'Unauthorized', 401
    data = request.get_json()

    food = Food( parent=ndb.Key(Food, claims['sub']), message=data['message'], food=data['food'], calories=data['calories'])
    food.friendly_id = claims.get('email', claims.get('email', 'Unknown'))
    food.put()

    return 'OK', 200

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500