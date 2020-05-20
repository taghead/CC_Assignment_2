import webapp2
from webapp2_extras import sessions
from google.appengine.ext import ndb
from google.appengine.api import users

# Variables
import_html=""

def get_one_entity(user_id):
    key = ndb.Key('user', user_id)
    return User.query(User.id == key).fetch()[0]

def googleUser(user):
            user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

class User(ndb.Model):
    id = ndb.KeyProperty(indexed=True)
    name = ndb.StringProperty(indexed=True)
    #password = ndb.IntegerProperty(indexed=True)
    password = ndb.StringProperty(indexed=True)

# Test Datastore Entry
key = ndb.Key('user', 10101)
p = User(id = key, name='Arthur Dent', password="a")
k = p.put()


class SessionHandler(webapp2.RequestHandler):
    def dispatch(self):
        import_html=self.response.write("""
        <link rel="stylesheet" href="/bootstrap/css/bootstrap.min.css"/>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
        <style>
            html {
                background-color: tomato;
            }
    
            body {
                margin: auto;
                width: 1000px;
            }
    
            nav {
                height: 30px;
                border-bottom: 1px solid black;
            }
    
            td {
                border: 1px solid black;
            }
        </style>

        """)
        googleUser(user)
        self.session_store = sessions.get_store(request=self.request)
        try: webapp2.RequestHandler.dispatch(self)
        finally: self.session_store.save_sessions(self.response)
    @webapp2.cached_property
    def session(self): return self.session_store.get_session()

class Index(SessionHandler): 
    def get(self): self.redirect('/login.php') 

class Login(SessionHandler):     
    def get(self): 
        import_html
        self.response.write("""
        <form method="post" class="p-3 mb-2 bg-primary text-white">
            <div class="form-group row">
                <label for="staticEmail" class="col-sm-2 col-form-label">Email</label>
                <div class="col-sm-10">
                    <input type="text" name="id" readonly class="form-control-plaintext" id="staticEmail"
                        value="email@example.com">
                </div>
            </div>
            <div class="form-group row">
                <label for="inputPassword" class="col-sm-2 col-form-label">Password</label>
                <div class="col-sm-10">
                    <input type="password" name="password" class="form-control" id="inputPassword" placeholder="Password">
                </div>
            </div>
            <div class="text-center">
                <button type="submit" class="btn btn-primary mb-2">Confirm identity</button>
            </div>
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

config = { 'webapp2_extras.sessions': { 'secret_key': 'key', } }

app=webapp2.WSGIApplication([ ('/', Index), ('/login.php',Login), ('/main.php', Main), ('/password.php', Password), ('/name.php', Name) ],config=config, debug=True)

def main(): app.run()

if __name__ == "__main__": main()