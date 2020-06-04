from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    RichMenu,
    RichMenuSize,
    RichMenuArea,
    RichMenuBounds,
    MessageAction,
    PostbackTemplateAction
)

def createRichmenu(line_bot_api):
    result = False
    try:
        rich_menu_to_create = RichMenu(
            size = RichMenuSize(width=1000, height=688),
            selected = True,
            name = 'richmenu for randomchat',
            chat_bar_text = 'メニュー',
            areas=[
                RichMenuArea(
                    bounds=RichMenuBounds(x=500, y=0, width=500, height=688),
                    action=MessageAction(text="Recipatorをはじめる")
                ),
            ]
        )
        richMenuId = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)

        path = './images/hungry.png'
        # path = './images/menu.png'

        with open(path, 'rb') as f:
            line_bot_api.set_rich_menu_image(richMenuId, "image/png", f)

        # set the default rich menu
        line_bot_api.set_default_rich_menu(richMenuId)

        result = True

    except Exception:
        result = False

    return result