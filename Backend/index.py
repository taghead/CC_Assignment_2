import logging

from flask import Flask, jsonify, request
import flask_cors
from google.appengine.ext import ndb
import google.auth.transport.requests
import google.oauth2.id_token
import requests_toolbelt.adapters.appengine

#import os
#import urllib
#import logging
#import flask_cors
#import google.auth.transport.requests
#import google.oauth2.id_token
#import requests_toolbelt.adapters.appengine
#
#from flask import Flask, jsonify, request
#from google.appengine.api import users
from google.appengine.ext import ndb

requests_toolbelt.adapters.appengine.monkeypatch()
HTTP_REQUEST = google.auth.transport.requests.Request()

app = Flask(__name__)
flask_cors.CORS(app)

# Datastore Models
class Note(ndb.Model):
    friendly_id = ndb.StringProperty()
    message = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

class Account(ndb.Model):
    email = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=True) 

class AccountFood(ndb.Model):
    account = ndb.StructuredProperty(Account)
    food = ndb.StringProperty(indexed=True)
    calories = ndb.StringProperty(indexed=True)

def query_database(user_id):
    ancestor_key = ndb.Key(Note, user_id)
    query = Note.query(ancestor=ancestor_key).order(-Note.created)
    notes = query.fetch()
    
    note_messages = []

    for note in notes:
        note_messages.append({
            'friendly_id': note.friendly_id,
            'message': note.message,
            'created': note.created
        })

    return note_messages

@app.route('/notes', methods=['GET'])
def list_notes():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401
    notes = query_database(claims['sub'])
    return jsonify(notes)

@app.route('/notes', methods=['POST', 'PUT'])
def add_note():
    id_token = request.headers['Authorization'].split(' ').pop()
    claims = google.oauth2.id_token.verify_firebase_token(
        id_token, HTTP_REQUEST)
    if not claims:
        return 'Unauthorized', 401
    data = request.get_json()
    note = Note(
        parent=ndb.Key(Note, claims['sub']),
        message=data['message'])
    note.friendly_id = claims.get('name', claims.get('email', 'Unknown'))
    note.put()

    return 'OK', 200

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500