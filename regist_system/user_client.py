from flask import Flask, render_template, request, redirect, url_for, flash
import requests, nfc, binascii

app = Flask(__name__)
app.secret_key = 'your_secret_key'
API_URL = "http://127.0.0.1:5000"  # Web API の URL


@app.route('/')
def index():
    response = requests.get(f"{API_URL}/users")
    users = response.json()
    return render_template('users.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    username = request.form.get('username')
    number = request.form.get('number')
    # /idm_inputにリダイレクト
    return render_template('idm_input.html', username=username, number=number)

@app.route('/idm_input', methods=['POST'])
def idm_input():
    username = request.form.get('username')
    number = request.form.get('number')
    flash('学生証をタッチしてください')
    idm_univ = get_IDm()
    # 前のフォームからユーザー名と番号を取得
    return render_template('idm_input_bus.html', username=username,number=number,idm_univ=idm_univ)

@app.route('/idm_input_bus', methods=['POST'])
def idm_input_bus():
    # 前のフォームからユーザー名と番号を取得
    username = request.form.get('username')
    number = request.form.get('number')
    idm_univ = request.form.get('idm_univ')
    flash('バスカードをタッチしてください')
    idm_bus = get_IDm()
    # 収集した情報をAPIに送信
    requests.post(f"{API_URL}/users", json={'username': username, 'number': number, 'idm_univ': idm_univ, 'idm_bus': idm_bus})
    # インデックスページにリダイレクト
    return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    requests.delete(f"{API_URL}/users/{user_id}")
    return redirect(url_for('index'))

def get_IDm():
    global idm
    try:
        # USB接続
        clf = nfc.ContactlessFrontend('usb')  # リーダーの接続確認
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        idm = binascii.hexlify(tag.identifier).upper()
        idm = idm.decode()
        return idm
    except AttributeError:
        print("error")

if __name__ == '__main__':
    app.run(port=8000)
