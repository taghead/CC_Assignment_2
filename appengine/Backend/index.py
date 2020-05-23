import os
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

class SQLQueryLog(ndb.Model):
    friendly_id = ndb.StringProperty()
    user_sql_query = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

def query_cloudsql(query):
    cloudsql_unix_socket = os.path.join(
        '/cloudsql', CLOUDSQL_CONNECTION_NAME)
    db = MySQLdb.connect(
        unix_socket=cloudsql_unix_socket,
        user=CLOUDSQL_USER,
        passwd='1234',
        db='wellbeingapp')
    cursor = db.cursor()
    cursor.execute(query)

    results = []
    for r in cursor.fetchall():
        results.append(r)
    return results


@app.route('/SQL_query', methods=['GET'])
def sql_query():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims: return 'Unauthorized', 401

    ancestor_key = ndb.Key(SQLQueryLog, claims['sub'])
    query = SQLQueryLog.query(ancestor=ancestor_key).order(-SQLQueryLog.created)
    food = str(query.fetch()[0].user_sql_query)

    q = query_cloudsql('select id, name, calories from FoodDataset WHERE upper(name) LIKE \'%'+food+'%\' LIMIT 5;')
    q_list = []
    for r in q:
        q_list.append({
            'friendly_id': str(r[0]),
            'food': str(r[1]),
            'calories': str(r[2])
        })
    print(q_list)
    return(jsonify(q_list))

@app.route('/add_query', methods=['POST', 'PUT'])
def add_query():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
    if not claims: return 'Unauthorized', 401
    data = request.get_json()

    query = SQLQueryLog( parent=ndb.Key(SQLQueryLog, claims['sub']), user_sql_query=data['query'])
    query.friendly_id = claims.get('email', claims.get('email', 'Unknown'))
    query.put()

    return 'OK', 200
    

#@app.route('/search_food', methods=['GET'])
#def search_food():
#    id_token = request.headers['Authorization'].split(' ').pop()
#    claims = google.oauth2.id_token.verify_firebase_token(id_token, HTTP_REQUEST)
#    if not claims: return 'Unauthorized', 401
#
#    data = request.get_json()
#    q = query_cloudsql('select id, name, calories from FoodDataset WHERE upper(name) LIKE \'%'+data['query']+'%\' LIMIT 10;')
#    q_list = []
#    for r in q:
#        q_list.append({
#            'friendly_id': str(r[0]),
#            'food': str(r[1]),
#            'calories': str(r[2])
#        })
#    print(q_list)
#    return(jsonify(q_list))

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