from flask import Flask, render_template, redirect, request, url_for
import sqlite3,requests
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
login_manager = LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = os.urandom(24)

@app.before_request
def create_tables():
    db.create_all()

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/',methods=['GET','POST'])
def signin():
    if request.method == 'POST':

        USER = request.form.get('username')
        PASSWORD = request.form.get('password')

        user = User(username=USER,password=generate_password_hash(PASSWORD,method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('check'))
    
    else:
        return render_template('top.html')

@app.route('/check',methods=['GET','POST'])
def login():
    if request.method == '':

        USER = request.form.get('username')
        PASSWORD = request.form.get('password')

        user = User.query.filter_by(username=USER).first()
        if check_password_hash(user.password,PASSWORD):
            login_user(user)
            return redirect(url_for('top'))
        else:
            return redirect(url_for('check'))
    
    else:
        return render_template('top.html')
        '''user = Users.query.filter_by(username=username).first()
        if check_password_hash(user.password, password):
            login_user(user)
            return redirect('/top')
    else:
        return render_template('top.html')




    '''
@app.route('/top',methods=['GET','POST'])
def top():
    return render_template('personal.html')


if __name__ == '__main__':
    app.run(port=8000)
