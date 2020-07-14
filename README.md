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
scikit-learn == 0.23.1
```

### 環境構築
```
$ pipenv install -r ./requirements.txt --skip-lock
```

新たなライブラリ入れたい場合は`requirements.txt`に書いて上記のコマンドを実行


## LINE BOT
### ローカルでの確認
// MARK: これは今後できなさそう
```
$ brew cask install ngrok
$ pipenv run python3 run.py
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
$ heroku config:set CHANNEL_ACCESS_TOKEN=<.envに書いてあるもの>
$ heroku config:set CHANNEL_SECRET=<.envに書いてあるもの>
$ heroku open
```
`heroku open` でhello worldが出てきたらデプロイ成功

## Recommend

## tree.pyの実行方法
```
$ pipenv run python3 tree.py
```
