from flask import Flask,request,render_template,redirect,url_for
import requests,qrcode
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(nullable=False)

@app.route('/',methods = ['GET'])
def home():
    return render_template('top.html')

@app.route('/login',methods = ['POST'])
def create_qr():
    username = request.form.get('username')
    password = request.form.get('password')
    data = [username,password]
    img = qrcode.make(data)
    img.save('test.png')
    return redirect(url_for('top'))

@app.route('/top',methods = ['GET'])
def top():
    return render_template("personal.html")

if __name__ == '__main__':
    app.run(port=8000)