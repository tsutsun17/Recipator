
import os
import settings
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
    TextMessage,
    TextSendMessage,
)

CHANNEL_ACCESS_TOKEN = settings.CHANNEL_ACCESS_TOKEN
CHANNEL_SECRET = settings.CHANNEL_SECRET

app = Flask(__name__)

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# rich menu
rich_menu_list = line_bot_api.get_rich_menu_list()
if not rich_menu_list:
    result = richmenu.createRichmeu(line_bot_api)
    if not result:
        reply.reply_message(event, "FAILED")

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
    line_bot_api.reply_message(
        event.reply_token,
        # TextSendMessage(text=event.message.text)
        TextSendMessage(text='返事しています')
    )

if __name__ == "__main__":
    app.run()