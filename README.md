# Recipator

## bot
### バージョン
```
python==3.7
line-bot-sdk==1.16.0
flask==1.1.2
```

### インストール
```
$ pipenv install -r ./requirements.txt
```

## herokuにデプロイ
```
$ heroku login
$ git push heroku master
$ heroku open
```
`heroku open` でhello worldが出てきたらデプロイ成功