from flask import Flask , render_template , request 
from ldap3 import Server, Connection, ALL
from flask_login import LoginManager, loginrequired , login_user

app = Flask(__name__)
login_manager = LoginManager()


def user_password_exist(username, password):

    exist=False
    user_full_name = "Nanashi"    

    # LDAP で認証
    server_uri = 'ldaps://tcs11.edu.kutc.kansai-u.ac.jp'
    user_dn = f'uid={username},ou=People,dc=kutc,dc=kansai-u,dc=ac,dc=jp'
    
    s = Server(server_uri, get_info=ALL)
    c = Connection(s, user=user_dn, password=password,  check_names=True, lazy=False)
    ret = c.bind()

    if ret==True:
        exist=True
        search_base = 'dc=kutc,dc=kansai-u,dc=ac,dc=jp'
        search_filter = f'(uid={username})'
        c.search(search_base, search_filter, attributes=['gecos'])
        #print( c.response)
        entry = c.entries[0]
        user_full_name = str(entry.gecos)
        #print("認証OK")
    else:
        exist=False
        #print("認証エラー")
        #print(user_dn)
        #print(c.result)
    c.unbind()

    return exist, user_full_name


@app.route('/')
def top():
    return render_template('top.html')

@app.route('/login',methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    exist,user_full_name = user_password_exist(username,password)
    if exist==True:
        return render_template('personal.html')
    else:
        return render_template('top.html')
    
if __name__ == '__main__':
    app.run()
