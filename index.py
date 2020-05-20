import os
import urllib
import jinja2
import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
from webapp2_extras import sessions

JINJA_ENVIRONMENT = jinja2.Environment( loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'], autoescape=True)

# Datastore Models
class Account(ndb.Model):
    identity = ndb.StringProperty(indexed=True)
    email = ndb.StringProperty(indexed=True)
    password = ndb.StringProperty(indexed=True) 

class AccountFood(ndb.Model):
    account = ndb.StructuredProperty(Account)
    food = ndb.StringProperty(indexed=True)
    calories = ndb.StringProperty(indexed=True)

# SessionHandler
class SessionHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try: webapp2.RequestHandler.dispatch(self)
        finally: self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self): return self.session_store.get_session()

#Pages
class MainPage(SessionHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'user': user,
            'url': url,
            'url_linktext': url_linktext,
        }

        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

    def post(self):
        
        self.redirect('/')


config = { 'webapp2_extras.sessions': { 'secret_key': 'key', } }

app = webapp2.WSGIApplication([ ('/', MainPage)], debug=True)
