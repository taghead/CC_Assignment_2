import os
import cgi
import urllib
import webapp2
import jinja2
from webapp2_extras import sessions
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment( loader=jinja2.FileSystemLoader(os.path.dirname(__file__)), extensions=['jinja2.ext.autoescape'], autoescape=True)

# Firebase Config
from config import firebase_config  

def get_one_entity(user_id):
    key = ndb.Key('user', user_id)
    return User.query(User.id == key).fetch()[0]

class User(ndb.Model):
    email = ndb.KeyProperty(indexed=True)

class SessionHandler(webapp2.RequestHandler):
    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        try: webapp2.RequestHandler.dispatch(self)
        finally: self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self): return self.session_store.get_session()

class Index(SessionHandler): 
    def get(self): self.redirect('/login.php') 

class Login(SessionHandler):     
    def get(self):    
        template_values = {
            "config": firebase_config
        }
        self.response.write(JINJA_ENVIRONMENT.get_template('./templates/header.tpl').render(template_values)) 
        self.response.write(JINJA_ENVIRONMENT.get_template('./templates/index.tpl').render(template_values)) 
    def post(self):
        self.redirect('/main.php') 

class SetSessionEmail(SessionHandler):     
    def get(self):    
        template_values = {
            "config": firebase_config
        }
        self.response.write(JINJA_ENVIRONMENT.get_template('./templates/header.tpl').render(template_values)) 
        self.response.write(JINJA_ENVIRONMENT.get_template('./templates/set_email.tpl').render(template_values)) 
    def post(self):
        print("GET EMAIL:"+self.request.get('email'))
        self.redirect('/main.php')  

class Main(SessionHandler):     
    def get(self):    
        template_values = {
            "config": firebase_config
        }
        self.response.write(JINJA_ENVIRONMENT.get_template('./templates/header.tpl').render(template_values)) 
        self.response.write(JINJA_ENVIRONMENT.get_template('./templates/main.tpl').render(template_values)) 
        
config = { 'webapp2_extras.sessions': { 'secret_key': 'key', } }
app=webapp2.WSGIApplication([ ('/', Index), ('/SetSessionEmail.php', SetSessionEmail) ,('/login.php',Login), ('/main.php',Main)],config=config, debug=True)
def main(): app.run()
if __name__ == "__main__": main()