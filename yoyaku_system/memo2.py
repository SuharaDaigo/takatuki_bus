from flask import Flask, render_template, redirect, request
import requests,sqlite3
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(32)

db = SQLAlchemy(app)

@login_manager.user_loader

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(db.String(50))

@app.before_request
def create_tables():
    db.create_all()    

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/')
def login():
    return render_template('top.html')

@app.route('/check',methods=['GET','POST'])
def check():
    username = request.form.get('username')
    password = request.form.get('password')
    
    
    user = Users.query.filter_by(username=username).first()
    if password(Users.password, password):
        login_user(user)
        return redirect('top')
    else:
        return render_template('top.html')


    #if(id=='k420762' and password =='Meteor1123'):
    #    return render_template('top.html.html')

@app.route('/top',methods=['POST'])
def top():
    return render_template('personnal.html')


if __name__ == '__main__':
    app.run(port=8000)
