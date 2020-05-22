import logging
import MySQLdb
import flask_cors
from flask import Flask, jsonify, request
import requests_toolbelt.adapters.appengine
import google.auth.transport.requests
import google.oauth2.id_token
from google.appengine.ext import ndb

requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)

CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
CLOUDSQL_PASSWORD = os.environ.get('1234')

class Food(ndb.Model):
    friendly_id = ndb.StringProperty()
    food = ndb.TextProperty()
    calories = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

def connect_to_cloudsql():
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
        cloudsql_unix_socket = os.path.join(
            '/cloudsql', CLOUDSQL_CONNECTION_NAME)
        db = MySQLdb.connect(
            unix_socket=cloudsql_unix_socket,
            user=CLOUDSQL_USER,
            passwd='1234',
            db='wellbeingapp')
    else:
        db = MySQLdb.connect(
            host='127.0.0.1', user=CLOUDSQL_USER, passwd='1234')
    return db

@app.route('/search_food'):
def search_food():
        id_token = request.headers['Authorization'].split(' ').pop()
        claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
        if not claims: return 'Unauthorized', 401

        data = request.get_json()
        db = connect_to_cloudsql()
        cursor = db.cursor()
        cursor.execute('select name from FoodDataset LIMIT 10;')

        results = []
        for r in cursor.fetchall():
            results.append({
                "id": r[0],
                "food": r[1],
                "calories": r[2]
            })
        return jsonify(results)

@app.route('/food', methods=['GET'])
def list_food():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims: return 'Unauthorized', 401

    ancestor_key = ndb.Key(Food, claims['sub'])
    query = Food.query(ancestor=ancestor_key).order(-Food.created)
    food = query.fetch()
    
    list_of_food = []
    for f in food:
        list_of_food.append({
            'friendly_id': f.friendly_id,
            'food': f.food,
            'calories': f.calories,
            'created': f.created
        })
        
    return jsonify(list_of_food)

@app.route('/add_food', methods=['POST', 'PUT'])
def add_food():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims: return 'Unauthorized', 401
    data = request.get_json()

    food = Food( parent=ndb.Key(Food, claims['sub']), food=data['food'], calories=data['calories'])
    food.friendly_id = claims.get('email', claims.get('email', 'Unknown'))
    food.put()

    return 'OK', 200

@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500