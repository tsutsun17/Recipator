# Recipator

## bot
### バージョン
```
python==3.7
line-bot-sdk==1.16.0
flask==1.1.2
```

### 環境構築
```
$ pipenv install -r ./requirements.txt
```

## herokuにデプロイ
```
$ heroku login
$ git push heroku master
$ heroku ps:scale web=1
$ heroku config:set CHANNEL_ACCESS_TOKEN=<.envに書いてあるもの>
$ heroku config:set CHANNEL_SECRET=<.envに書いてあるもの>
$ heroku open
```
`heroku open` でhello worldが出てきたらデプロイ成功