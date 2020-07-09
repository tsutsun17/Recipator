
import os
import settings, richmenu, tree
from flask import (
    Flask,
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

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

questions = tree.QuestionsClass()

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
    answer_list = ["Yes", "No"]
    items = [QuickReplyButton(action=MessageAction(label=f"{answer}", text=f"{answer}")) for answer in answer_list]
    print(questions)

    if event.message.text == 'Recipatorをはじめる':
        global questions
        questions = tree.QuestionsClass(status=1)
        status, body = questions.call_first_question()

        messages = TextSendMessage(text=body, quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
    else:
        # questionsのstatusが1出ない: 「Recipatorをはじめる」を押していない場合
        if questions.status!=1:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='メニューから「Recipatorをはじめる」を押してみてね！')
            )
            return

        print(event.message.text)
        # ボタンを押していない場合
        if event.message.text!="Yes" and event.message.text!="No":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='ボタンを押して回答してね！')
            )
            return

        # 1: Yes, 0: No
        ans = 1 if event.message.text == "Yes" else 0

        status, body = questions.cal_current_node(ans)

        if status=='question':
            messages = TextSendMessage(text=body, quick_reply=QuickReply(items=items))
            line_bot_api.reply_message(event.reply_token, messages=messages)
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='フォローありがとう！ \nメニューから「Recipatorをはじめる」を押してみてね！')
    )

if __name__ == "__main__":
    app.run()
