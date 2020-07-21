from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import (
    TemplateSendMessage,
    CarouselTemplate,
    CarouselColumn
)

from line_app.models import Recipe

def setRecipeCarouseColumn(recipe):
    column = CarouselColumn(
        thumbnail_image_url=recipe.image_url,
        title=recipe.name,
        text='美味しいよ',
        actions=[
            {
                'type': 'uri',
                'label': 'レシピをみる',
                'text': recipe.recipe_url
            }
        ]
    )

    return column

def setRecipeCarouse(recipes):
    notes = [setRecipeCarouseColumn(recipe) for recipe in recipes]

    return notes

def setTemplateSendMessage(recipes):
    messages = TemplateSendMessage(
        alt_text='template',
        template=CarouselTemplate(columns=setRecipeCarouse(recipes))
    )

    return messages
