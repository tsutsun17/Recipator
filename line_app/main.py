
import os
import tree
from line_app import *
import line_app.richmenu as richmenu
import line_app.settings as settings

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
    QuickReply,
    TemplateSendMessage,
    CarouselTemplate,
    CarouselColumn
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
    users = db.session.query(User).all()
    print(vars(users))
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
    user = db.session.query(User).filter(
        User.line_user_id == user_id).limit(1).all()
    user = user[0]

    answer_list = ["Yes", "No"]
    items = [QuickReplyButton(action=MessageAction(
        label=f"{answer}", text=f"{answer}")) for answer in answer_list]

    if event.message.text == 'Recipatorをはじめる':
        user.status = 1
        user.current_node = 0
        db.session.add(user)
        db.session.commit()

        questions = tree.QuestionsClass()
        status, body = questions.call_first_question()

        messages = TextSendMessage(
            text=body, quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
        return

    # userのstatusが1でない: 「Recipatorをはじめる」を押していない場合
    if user.status != 1:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='メニューから「Recipatorをはじめる」を押してみてね！')
        )
        return

    # ボタンを押していない場合
    if event.message.text != "Yes" and event.message.text != "No":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='ボタンを押して回答してね！')
        )
        return

    # 1: Yes, 0: No
    ans = 1 if event.message.text == "Yes" else 0

    questions = tree.QuestionsClass(current_node=user.current_node)
    status, body = questions.cal_current_node(ans)

    # current_nodeの更新
    current_node = questions.current_node
    user.current_node = int(current_node)
    db.session.add(user)
    db.session.commit()

    if status == 'question':
        messages = TextSendMessage(
            text=body, quick_reply=QuickReply(items=items))
        line_bot_api.reply_message(event.reply_token, messages=messages)
        return

    if status == 'recipes':
        # notes = [
        #     CarouselColumn(
        #         thumbnail_image_url="https://jp.rakuten-static.com/recipe-space/d/strg/ctrl/3/38a48fa0dab1e95c961ae0886c7371935eedbd81.04.2.3.2.jpg?thum=58",
        #         title="夏野菜の和風パスタ",
        #         text="おいしいよ",
        #         actions=[
        #             {"type": "message",
        #              "label": "レシピを見る",
        #              "text": "https://recipe.rakuten.co.jp/recipe/1740021616"}]),

        #     CarouselColumn(
        #         thumbnail_image_url="https://jp.rakuten-static.com/recipe-space/d/strg/ctrl/3/38a48fa0dab1e95c961ae0886c7371935eedbd81.04.2.3.2.jpg?thum=58",
        #         title="カニ缶とわかめのパスタ",
        #         text="材料がおおいよ",
        #         actions=[
        #             {"type": "message",
        #              "label": "レシピを見る",
        #              "text": "https://cookpad.com/recipe/6359468"}])
        # ]
        # messages = TemplateSendMessage(
        #     alt_text='template',
        #     template=CarouselTemplate(columns=notes),
        # )
        # line_bot_api.reply_message(event.reply_token, messages=messages)
        # return

    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=event.message.text)
    # )


@handler.add(FollowEvent)
def handle_follow(event):
    # TODO: ここでユーザー情報登録
    user_id = event.source.user_id
    user = User(status=0, line_user_id=user_id, current_node=0)
    db.session.add(user)
    db.session.commit()

    notes = [
        CarouselColumn(thumbnail_image_url="https://jp.rakuten-static.com/recipe-space/d/strg/ctrl/3/38a48fa0dab1e95c961ae0886c7371935eedbd81.04.2.3.2.jpg?thum=58",
                       title="夏野菜の和風パスタ",
                       text="おいしいよ",
                       actions=[
                           {"type": "message",
                            "label": "レシピを見る",
                            "text": "https://recipe.rakuten.co.jp/recipe/1740021616/"}]),

        CarouselColumn(thumbnail_image_url="https://jp.rakuten-static.com/recipe-space/d/strg/ctrl/3/38a48fa0dab1e95c961ae0886c7371935eedbd81.04.2.3.2.jpg?thum=58",
                       title="カニ缶とわかめのパスタ",
                       text="材料がおおいよ",
                       actions=[
                           {"type": "message",
                            "label": "レシピを見る",
                            "text": "https://cookpad.com/recipe/6359468"}])
    ]
    messages = TemplateSendMessage(
        alt_text='template',
        template=CarouselTemplate(columns=notes)
    )
    line_bot_api.reply_message(event.reply_token, messages=messages)
    return


if __name__ == "__main__":
    app.run(debug=True)
