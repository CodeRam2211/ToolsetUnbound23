from flask import Flask, render_template,request,url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")
@app.route('/dashboard')
def dashboard() :
    return render_template('dashboard.html')
@app.route('/files')
def files():
    return render_template('files.html')


if __name__ == '__main__':
    app.run(debug = True)