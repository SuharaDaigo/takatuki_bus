# memo for sample_user_app


まず以下をインストールしておいてください．
```bash
pip install flask
pip install flask_sqlalchemy
```

この例では，サーバー側でユーザー登録，削除，一覧情報のための WebAPI を提供し，クライアント側からサーバにアクセスしてそのAPIを利用してユーザーの登録，削除，一覧を表示するようにしています．

```bash
python user_server.py
```

でサーバー側のプログラムを起動し，

```bash
python user_client.py
```

でクライアント側のプログラムを起動し，[http://127.0.0.1:8000](http://127.0.0.1:8000) にアクセスすることで見ることができます．