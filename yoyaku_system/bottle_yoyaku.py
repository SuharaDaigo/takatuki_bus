from bottle import Bottle, route, run, template, request
import sqlite3

# SQLite3データベースに接続
conn = sqlite3.connect('yoyaku_seki.db')
cursor = conn.cursor()

# テーブルが存在しない場合は作成
cursor.execute('''
    CREATE TABLE IF NOT EXISTS yoyaku_seki (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        seat_number INTEGER
    )
''')
conn.commit()

app = Bottle()

@app.route('/')
def index():
    cursor.execute('SELECT seat_number FROM yoyaku_seki')
    yoyaku_seki = [row[0] for row in cursor.fetchall()]
    return template('index', yoyaku_seki=yoyaku_seki)

@app.route('/yoyaku', method='POST')
def yoyaku():
    seat_number = int(request.forms.get('seat_number'))

    # 席がすでに予約されているか確認
    cursor.execute('SELECT seat_number FROM yoyaku_seki WHERE seat_number = ?', (seat_number,))
    existing_reservation = cursor.fetchone()

    if existing_reservation:
        print(f"席{seat_number}の予約が失敗しました")
        return "予約失敗"
    else:
        # 席を予約する
        cursor.execute('INSERT INTO yoyaku_seki (seat_number) VALUES (?)', (seat_number,))
        conn.commit()
        print(f"席{seat_number}が予約されました！")
        return "予約完了"

if __name__ == "__main__":
    run(app, host='localhost', port=8080, reloader=True, debug=True)
