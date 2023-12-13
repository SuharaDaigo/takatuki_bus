from flask import Flask, request, jsonify,make_response,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager,UserMixin
from flask import abort
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

username = 'none'
password = 'none'
true_password = 'none'

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    password = db.Column(nullable=False)

    
@app.before_request
def limit_access():
    allowed_ips = ['127.0.0.1']
    if request.remote_addr not in allowed_ips:
        abort(403)


@app.route('/check',methods=['POST'])
def check_login():
    data = request.get_json()
    user_data = User(username=data['username'], password=data['password'])
    user = User.query.filter_by(username=user_data.username).first()
    global username,password,true_password
    true_password = user.password
    username = user_data.username
    password = user_data.password
    return jsonify({f'message': ' created successfully.'}), 201

@app.route('/check_return',methods=['GET'])
def check_return():
    print(username,password,true_password)
    data = [password,true_password]
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
