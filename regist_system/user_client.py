from flask import Flask, render_template, request, redirect, url_for, flash
import requests, nfc, binascii

app = Flask(__name__)
app.config['SECRET_KEY'] = '0000'
API_URL = "http://127.0.0.1:5000"  # Web API の URL


@app.route('/')
def index():
    response = requests.get(f"{API_URL}/users")
    users = response.json()
    return render_template('2_menu.html')


@app.route('/scan', methods=['GET'])
def scan():
    return render_template('3_scan.html')


@app.route('/teiki_scan', methods=['POST'])
def add_user():
    return render_template('4_teiki_scan.html')


@app.route('/input_idm_bus', methods=['POST'])
def idm_input_bus():
    idm_bus = get_bus()
    return render_template('5_release.html', idm_bus = idm_bus)


@app.route('/release', methods=['POST'])
def release():
    idm_bus = request.form.get('idm_bus')
    return render_template('6_studentcard_scan.html', idm_bus = idm_bus)


@app.route('/input_idm_univ', methods=['POST'])
def idm_input():
    # 前のフォームからユーザー名と番号を取得
    idm_bus = request.form.get('idm_bus')
    student_id,idm_univ = get_univ()
    # busとunivのidmが一致してたら初めからやり直し
    if idm_univ == idm_bus :
        return redirect(url_for('index'))
    else :
        # 収集した情報をAPIに送信
        response = requests.post(f"{API_URL}/users", json={'student_id': student_id,'idm_univ': idm_univ, 'idm_bus': idm_bus})
        # データに重複があった場合はエラーページにリダイレクト
        status_code = response.status_code
        if status_code == 401:
            message = "この学生証はすでに登録されています"
            return render_template('8_error.html', message = message)
        elif status_code == 402:
            message = "このバス定期券はすでに登録されています"
            return render_template('8_error.html', message = message)
        # 登録完了ページにリダイレクト
        return render_template('7_complete.html', student_id = student_id)

# ユーザー削除用関数(使わないかも)
@app.route('/delete', methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    requests.delete(f"{API_URL}/users/{user_id}")


# 学生証スキャン用関数
def get_univ():
    clf = nfc.ContactlessFrontend('usb')
    tag = clf.connect(rdwr={'on-connect': lambda tag: False})

    idm, pmm = tag.polling(system_code=0xfe00)
    tag.idm, tag.pmm, tag.sys = idm, pmm, 0xfe00

    service_code = [nfc.tag.tt3.ServiceCode(106, 0x0b)]
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


# バス定期スキャン用関数
def get_bus():
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
