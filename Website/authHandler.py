from flask import Flask,Blueprint,render_template,redirect, url_for,request
from werkzeug.security import generate_password_hash,check_password_hash

auth = Flask(__name__)

