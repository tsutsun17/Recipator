
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
    user_id = event.source.user_id
    users = User.find_by_line_user_id(user_id)
    if len(users)==0:
        user = User(status=0, line_user_id=user_id, current_node=0)
        user.commit_db()
    else:
        user = users[0]

    answer_list = ["Yes", "No"]
    items = [QuickReplyButton(action=MessageAction(label=f"{answer}", text=f"{answer}")) for answer in answer_list]

    if event.message.text == 'Recipatorをはじめる':
        user.status = 1
        user.current_node = 0
        user.commit_db()

        questions = tree.QuestionsClass()
        status, body = questions.get_current_question()

        messages = TextSendMessage(text=body, quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
        return
    
    # userのstatusが1でない: 「Recipatorをはじめる」を押していない場合
    if user.status!=1:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='メニューから「Recipatorをはじめる」を押してみてね！')
        )
        return

    questions = tree.QuestionsClass(current_node=user.current_node)

    # ボタンを押していない場合
    if event.message.text!="Yes" and event.message.text!="No":
        status, body = questions.get_current_question()
        messages = TextSendMessage(text=body, quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
        return

    # 1: Yes, 0: No
    ans = 1 if event.message.text == "Yes" else 0
    status, body = questions.cal_current_node(ans)

    # current_nodeの更新
    current_node = questions.current_node
    user.current_node = int(current_node)
    user.commit_db()

    if status=='question':
        messages = TextSendMessage(text=body, quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
        return

    if status=='recipes':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='//TODO: レシピ一覧')
        )
        # TODO: 一旦、レシピ一覧を出したら終了することにする
        user.status = 0
        user.commit_db()
        return

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    users = User.find_by_line_user_id(user_id)
    if len(users)==0:
        user = User(status=0, line_user_id=user_id, current_node=0)
        user.commit_db()

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='フォローありがとう！ \nメニューから「Recipatorをはじめる」を押してみてね！')
    )

if __name__ == "__main__":
    app.run(debug=True)
