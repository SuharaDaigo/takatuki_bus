from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String, nullable=False)
    idm_univ = db.Column(db.String(20), nullable=False)
    idm_bus = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        return f"<User {self.username}>"

@app.before_request
def create_tables():
    db.create_all()

#許可するIPアドレスを指定
@app.before_request
def limit_access():
    allowed_ips = ['127.0.0.1']
    if request.remote_addr not in allowed_ips:
        abort(403)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(username=data['username'],number=data['number'],password=data['password'],idm_univ=data['idm_univ'],idm_bus=data['idm_bus'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully.'}), 201

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully.'})

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'number': user.number, 'password':user.password, 'idm_univ': user.idm_univ, 'idm_bus': user.idm_bus} for user in users])

if __name__ == '__main__':
    app.run(debug=True)
