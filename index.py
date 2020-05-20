import webapp2
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

### START TASK 1 ###
class Login(SessionHandler):     
    def get(self): 
        self.response.write("""
        <form method="post">
            User ID<input type="text" name="id"\>
            Password<input type="number" name="password"\>
            <input type="submit" value="Log In">
        </form>
        """)

    def post(self):
        self.session['id']=self.request.get('id')
        try:
            if ( str(get_one_entity(self.request.get('id')).password) == str(self.request.get('password'))):
                self.redirect('/main.php')
            else: raise IndexError()
        except IndexError: 
            self.response.out.write("User id or password is invalid")
### END TASK 1 ###

### START TASK 2 ###
class Main(SessionHandler):        
    def get(self): 
        self.response.write(get_one_entity(self.session.get('id')).name+"""
        <form method="post">
            <div><input type="submit" name='change_user' value="Change Name"></div>
            <div><input type="submit" name='change_password' value="Change Password"></div>
        </form>
        """)

    def post(self):
        if self.request.get('change_password'): self.redirect('/password.php')
        if self.request.get('change_user'): self.redirect('/name.php')  
### END TASK 2 ###

### START TASK 3 ###
class Name(SessionHandler):
    def get(self): 
        self.response.write("""
        <form method="post">
            New Name<input type="text" name="username" \>
            <input type="submit" name='change_username' value="Change">
        </form>
        """)

    def post(self):
        if( len((self.request.get('username')).replace(" ","")) < 1 ):
            self.response.write("User name cannot be empty")
        else:
            user_entity = get_one_entity(self.session.get('id'))
            user_entity.name = self.request.get('username')
            user_entity.put()
            self.redirect('/main.php')  
### END TASK 3 ###

### START TASK 4 ###
class Password(SessionHandler):    
    def get(self): 
        self.response.write("""
        <form method="post">
            Old Password<input type="number" name="old_password"\>
            New Password<input type="number" name="new_password"\>
            <input type="submit" name='change_password' value="Change">
        </form>
        """)
    
    def post(self):
        user_entity = get_one_entity(str(self.session.get('id')))
        if ( self.request.get('old_password') == str(user_entity.password) ):
            user_entity.password = int(str(self.request.get('new_password')))
            user_entity.put()
            self.redirect('/login.php')
        else: self.response.write('User password is incorrect')  
### END TASK 4 ###
config = { 'webapp2_extras.sessions': { 'secret_key': 'key', } }

app=webapp2.WSGIApplication([ ('/', Index), ('/login.php',Login), ('/main.php', Main), ('/password.php', Password), ('/name.php', Name) ],config=config, debug=True)

def main(): app.run()

if __name__ == "__main__": main()