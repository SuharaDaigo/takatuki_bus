from flask import Flask, render_template, request, redirect, url_for, flash
import requests, nfc, binascii
from werkzeug.security import generate_password_hash, check_password_hash

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
    # /idm_inputにリダイレクト
    return render_template('idm_input.html')

@app.route('/idm_input', methods=['POST'])
def idm_input():
    student_id,idm_univ = get_univ()
    return render_template('idm_input_bus.html', student_id = student_id, idm_univ = idm_univ)

@app.route('/idm_input_bus', methods=['POST'])
def idm_input_bus():
    # 前のフォームからユーザー名と番号を取得
    student_id = request.form.get('student_id')
    idm_univ = request.form.get('idm_univ')
    idm_bus = get_IDm()

    if idm_univ == idm_bus :
        return redirect(url_for('index'))
    else :
        # 収集した情報をAPIに送信
        requests.post(f"{API_URL}/users", json={'student_id': student_id,'idm_univ': idm_univ, 'idm_bus': idm_bus})
        # インデックスページにリダイレクト
        return redirect(url_for('index'))

@app.route('/delete', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    requests.delete(f"{API_URL}/users/{user_id}")
    return redirect(url_for('index'))

def get_univ():
    clf = nfc.ContactlessFrontend('usb')
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})

    idm, pmm = tag.polling(system_code=0xfe00)
    tag.idm, tag.pmm, tag.sys = idm, pmm, 0xfe00
        
    service_code = [nfc.tag.tt3.ServiceCode(106, 0x0b)]
    #bc_id = [nfc.tag.tt3.BlockCode(i) for i in range(4)]
    bc_id   = [nfc.tag.tt3.BlockCode(0)]
    bc_name = [nfc.tag.tt3.BlockCode(1)]

    student_id_data = tag.read_without_encryption(service_code, bc_id)
    name_data = tag.read_without_encryption(service_code, bc_name)

    student_id = student_id_data.decode('utf-8')
    student_id = student_id[8:14]
    name = name_data.decode('utf-8')

    idm = binascii.hexlify(tag.identifier).upper()
    idm = idm.decode()
 
    return student_id,idm


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
