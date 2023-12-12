from flask import Flask, render_template
from flask_login import LoginManager, UserMixin
import os

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(32)

@login_manager.user_loader


@app.route('/')
def login():
    return render_template('top.html')

if __name__ == '__main__':
    app.run(port=8000)
