from flask import Flask,Blueprint
from flask_login import LoginManager

app =  Flask(__name__)
  
    
login_managager = LoginManager()
login_managager.login_view = 'auth.login'
login_managager.init_app(app)

from authHandler import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import app as main_blueprint
app.register_blueprint(main_blueprint)

if(__name__ == '__main__'):
    app.run(debug=True)

