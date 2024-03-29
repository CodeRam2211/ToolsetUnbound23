from flask import Flask, render_template,request,url_for,flash,redirect
import sys
import getpass
import colorama
from colorama import Fore
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user
from werkzeug.security import generate_password_hash,check_password_hash
import mysql.connector as conn
#create User object for authentication

sys.path.insert(0,'../Databases')
import DBRequests

db =''
try:
    MySQLUser = input("Enter your username for mysql server :")
    MySQLPass = getpass.getpass("Enter your password")
    db = conn.connect(host="localhost",user=MySQLUser,passwd = MySQLPass,database="toolset")
except conn.ProgrammingError as e:
    print(Fore.RED+"Error Access Denied")
    print(Fore.RED+"Wrong username or password entered")

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
user = User({'id':'1','password':'password','username':'user'})
app = Flask(__name__)
app.secret_key = 'fri  lf oeijgrowa j' #change this key and set it t oa secret on used to prevent cookie tampering

login_manager = LoginManager() #flask_login object to authenticate everything
login_manager.init_app(app)

@app.route('/login',methods = ['POST'])
def login():
    #getting usernames and passwords of the user
    form = {'username': request.form.get('username'),'password':request.form.get('password')}
    print(form['username'])
    idMatch = DBRequests.search_username(form['username'],db)
    if(idMatch == None):
        flash("Error! Wrong Credentials entered")
        return render_template(template_name_or_list="index.html", data = "Invalid Credentials", d2="")
    user = User({'id':idMatch[0][0],'username':idMatch[0][1],'password':idMatch[0][2]})
    if(user.check_password(form['password'])):
        flash('Login Successful')
        login_user(user)
        return redirect(('/dashboard/'+str(form['username'])))
    return render_template(template_name_or_list="index.html", data = "Invalid Credentials", d2="")

@login_manager.user_loader
def load_user(user_id):
    #if id not in users
    return user

@app.route('/',)#home page containing login option
def index():
    return render_template("index.html")


@app.route('/compress')
@login_required
def compress():
    return render_template('text.html')

@app.route('/dashboard/<username>')
@login_required
def dashboard(username) :
    return render_template('dashboard.html', user = username)

@app.route('/files/<username>')
@login_required
def files(username):
    return render_template('files.html',fileList = [[1,2,3,4,5]])
@app.route('/signup')
def signUpLoad():
    return render_template('signup.html')
@app.route('/signupSend',methods = ['POST'])
def signUp():
    print("a")
    form = {'email':request.form.get('nemail'),'password':request.form.get('npas'),'username':request.form.get('nuser')}
    print(form['email'])
    if(DBRequests.insert(form['username'],form['password'],form['email'],db) == 1):
        print("signed up successfully")
    else:
        print(Fore.RED+"encountered some error")
    return redirect('/')
# @app.route('/text',methods = ['POST'])
# @login_required
# def textCompres():
    
@app.route("/logout")
@login_required
def logout():
    logout_user()

    return redirect('/')

    
if __name__ == '__main__':
    app.run(debug = True,host="0.0.0.0")
