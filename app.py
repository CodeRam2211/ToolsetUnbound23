from flask import Flask, render_template,request,url_for,flash,redirect

from flask_login import LoginManager,UserMixin,login_required,login_user
from werkzeug.security import generate_password_hash,check_password_hash

#create User object for authentication
class User(UserMixin):
    def __init__(self,vals):
        self.id = vals['id']
        self.username = vals['username']
        self.password_hash = ''
        self.set_password(vals['password'])
    def set_password(self,passw):
        self.password_hash = generate_password_hash(passw)
        return 1
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    def __repr__(self):
        return '<User %r>' % self.username


user = User({'id':1,'username':'user','password':'password'})
app = Flask(__name__)
app.secret_key = 'fri  lf oeijgrowa j' #change this key and set it t oa secret on used to prevent cookie tampering

login_manager = LoginManager() #flask_login object to authenticate everything
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user

@app.route('/')#home page containing login option
def index():
    return render_template("index.html")


@app.route('/compress')
@login_required
def compress():
    return render_template('text.html')

@app.route('/dashboard')
@login_required
def dashboard() :
    return render_template('dashboard.html')

@app.route('/files')
@login_required
def files():
    return render_template('files.html')

@app.route('/login',methods = ['POST'])
def login():
    form = {'username': request.form.get('username'),'password':request.form.get('password')}
    print(form['username'])
    if(user.check_password(form['password'])):
        flash('Login Successful')
        login_user(user)
        return redirect('/dashboard')
    return "wrong"
    
if __name__ == '__main__':
    app.run(debug = True)