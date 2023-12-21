from ldap3 import Server, Connection, ALL
import getpass,ssl

##################################################
#ユーザネームとパスワードが一致するかを判断
##################################################
def user_password_exist(username, password):

    exist=False
    user_full_name = "Nanashi"    

    # LDAP で認証
    server_uri = 'ldap://tcs11.edu.kutc.kansai-u.ac.jp'
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
    

if __name__=="__main__":
    print("LDAP認証のテスト")    
    username = input("k番を入力してください:")
    pwd = getpass.getpass(prompt = 'パスワードを入力してください:')
    print(username,pwd)
    exist, user_full_name = user_password_exist( username, pwd )
    
    if exist==True:
        print(f"認証されました． {user_full_name}さん，こんにちは！")
    else:
        print("認証に失敗しました")

