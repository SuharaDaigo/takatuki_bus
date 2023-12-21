from flask import Flask, request, jsonify, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = '0000'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), nullable=False)
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

#ユーザー登録用ルート
@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    #登録済みユーザーとの重複チェック
    user = User.query.filter_by(student_id=data['student_id']).first()
    if user:
        return jsonify({'message': 'スキャンした学籍番号はすでに登録されています'}), 401
    #バス定期券の重複チェック
    bus_teiki = User.query.filter_by(idm_bus=data['idm_bus']).first()
    if bus_teiki:
        return jsonify({'message': 'スキャンしたバス定期券はすでに登録されています'}), 402
    #重複なければデータベースに登録
    new_user = User(student_id=data['student_id'],idm_univ=data['idm_univ'],idm_bus=data['idm_bus'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'ユーザーの登録が完了しました'}), 201

#ユーザー消去用ルート(使わないかも)
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
    return jsonify([{'id': user.id, 'student_id': user.student_id, 'idm_univ': user.idm_univ, 'idm_bus':user.idm_bus} for user in users])

if __name__ == '__main__':
    app.run(debug=True)
