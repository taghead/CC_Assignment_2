import os
import webapp2
from google.appengine.ext.webapp import template
from webapp2_extras import sessions
from google.appengine.ext import ndb

def get_one_entity(user_id):
    key = ndb.Key('user', user_id)
    return User.query(User.id == key).fetch()[0]

class User(ndb.Model):
    id = ndb.KeyProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    password = ndb.IntegerProperty(indexed=True)

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
        self.response.write("""
        <form method="post">
            User ID<input type="text" name="id"\>
            Password<input type="number" name="password"\>
            <input type="submit" value="Log In">
        </form>
        """)
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'header.inc')
        self.response.out.write(template.render(path, template_values))
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
        

config = { 'webapp2_extras.sessions': { 'secret_key': 'key', } }

app=webapp2.WSGIApplication([ ('/', Index), ('/login.php',Login)],config=config, debug=True)

def main(): app.run()

if __name__ == "__main__": main()