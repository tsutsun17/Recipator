
import os
import tree
from line_app import *
import line_app.richmenu as richmenu, line_app.settings as settings

from line_app.models.user import User

from flask import (
    request,
    abort
)

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent,
    FollowEvent,
    TextMessage,
    TextSendMessage,
    QuickReplyButton,
    MessageAction,
    QuickReply
)

CHANNEL_ACCESS_TOKEN = settings.CHANNEL_ACCESS_TOKEN
CHANNEL_SECRET = settings.CHANNEL_SECRET

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# set rich menu
richmenu.createRichmenu(line_bot_api)


# herokuの確認用
@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # TODO: ここでユーザーのstatusを確認
    # users = db.session.query(User).\
    #     filter(User.name=="name").\
    #     all()
    answer_list = ["Yes", "No"]
    items = [QuickReplyButton(action=MessageAction(label=f"{answer}", text=f"{answer}")) for answer in answer_list]

    print(event)

    if event.message.text == 'Recipatorをはじめる':
        questions = tree.QuestionsClass()
        status, body = questions.call_first_question()

        messages = TextSendMessage(text=body, quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
        return
    
    # questionsのstatusが1出ない: 「Recipatorをはじめる」を押していない場合
    # TODO: statusで判断
    if questions.status!=1:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='メニューから「Recipatorをはじめる」を押してみてね！')
        )
        return

    # ボタンを押していない場合
    if event.message.text!="Yes" and event.message.text!="No":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='ボタンを押して回答してね！')
        )
        questions.status = 1
        return

    # 1: Yes, 0: No
    ans = 1 if event.message.text == "Yes" else 0

    status, body = questions.cal_current_node(ans)

    if status=='question':
        messages = TextSendMessage(text=body, quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
        questions.status = 1
        return

    if status=='recipes':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='//TODO: レシピ一覧')
        )
        questions.status = 0
        return

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text)
    # )

@handler.add(FollowEvent)
def handle_follow(event):
    # TODO: ここでユーザー情報登録
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='フォローありがとう！ \nメニューから「Recipatorをはじめる」を押してみてね！')
    )

if __name__ == "__main__":
    app.run(debug=True)
