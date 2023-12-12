from flask import Flask, render_template, request, redirect, url_for
import requests,  binascii
from flask_login import UserMixin, LoginManager, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
API_URL = "http://127.0.0.1:5000"  # Web API の URL


@app.route('/',methods=['POST','GET'])
def top():
        return render_template('top.html')

@app.route('/login',methods=['POST','GET'])
def login_check():
        if request.method=='POST':
            username = request.form.get('username')
            password = request.form.get('password')

            requests.post(f"{API_URL}/check", json={'username': username,'password':password})
            return redirect(url_for(f'login_result'))
        '''if(true_password==password):
            return render_template('personal.html',username=username)
        else:
              return redirect('/')'''


@app.route('/login_result',methods = ['GET'])
def login_result():
    response = requests.get(f"{API_URL}/check_return")
    user = response.json()
    hash_password = generate_password_hash(user[1],method='pbkdf2:sha256')
    print(hash_password)
    username = user[0]
    password = user[1]
    true_password = user[2]
    if check_password_hash(true_password,password):
          return render_template('personal.html',username=username)


'''@app.route('/login_success',methods=['POST','GET']
login_success(username):
    return render_template('personal.html',username=username)'''    

if __name__ == '__main__':
    app.run(port=8000)