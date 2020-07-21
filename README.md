# Recipator
### バージョン
```
line-bot-sdk == 1.16.0
Flask == 1.1.2
python-dotenv == 0.13.0
gunicorn == 20.0.4
numpy == 1.18.4
pandas == 0.24.1
pydotplus == 2.0.2
flask-sqlalchemy == 2.4.3
flask-migrate == 2.5.3
psycopg2 == 2.8.5

scikit-learn == 0.23.1
numpy == 1.18.4
pandas == 0.24.1
```

### 環境構築
```
$ pipenv install -r ./requirements.txt --skip-lock
```

新たなライブラリ入れたい場合は`requirements.txt`に書いて上記のコマンドを実行


#### Postgresqlの導入

```
$ brew install postgresql
```

* 新しい`.env`が必要

```
$ initdb /usr/local/var/postgres -E utf8    # DBの初期化
$ brew services start postgresql            # 起動
$ createuser -s -P recipator_root           # ユーザー登録
$ psql postgres                             # postgresに入る
postgres=# CREATE DATABASE "recipator_db" OWNER "recipator_root";   # DBの作成
postgres=# exit                             # postgresから出る
$ pipenv run flask db init                  # マイグレーションのための準備
$ pipenv run flask db migrate               # マイグレーション(Creates an automatic revision script.)
$ pipenv run flask db upgrade               # マイクレーション実行(Upgrades the database.)
$ pipenv run python3 db_seed.py             # Recipeデータの挿入
```

### DB（ローカル）のマイグレーション方法
```
$ pipenv run flask db migrate
$ pipenv run flask db upgrade
```

ロールバックは以下の通り
```
$ pipenv run flask db downgrade
```

### DB(ローカル)の確認
```
$ psql recipator_db
recipator_db=# \d   # テーブル確認
```

## LINE BOT
### ローカルでの確認
// MARK: これは今後できなさそう
```
$ brew cask install ngrok
$ pipenv run python3 app.py
```
別のターミナルで
```
$ ngrok http 5000
```
表示されるurlをLINE BOTのWebhook URLに使用する

※ これは`localhost`を公開するので割と危ない感じ

## herokuにデプロイ
この作業は`@szkn`だけが行う
```
$ heroku login
$ git push heroku master
$ heroku ps:scale web=1
$ heroku config:set CHANNEL_ACCESS_TOKEN=<.envに書いてあるもの> --app "recipator"
$ heroku config:set CHANNEL_SECRET=<.envに書いてあるもの> --app "recipator"
$ heroku config:set SQLALCHEMY_DATABASE_URI=<heroku postgres> --app "recipator"
$ heroku config:set SQLALCHEMY_TRACK_MODIFICATIONS=False --app "recipator"
$ heroku run:detached flask db upgrade
$ heroku run:detached python3 db_seed.py
$ heroku open
```
`heroku open` でhello worldが出てきたらデプロイ成功

## Recommend

## tree.pyの実行方法
```
$ pipenv run python3 tree.py
```
