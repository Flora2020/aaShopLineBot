from linebot.models import (
    TemplateSendMessage, ButtonsTemplate
)
from linebot.models.actions import (
    MessageAction
)


def get_menu():
    return TemplateSendMessage(
        alt_text=u'主選單',
        template=ButtonsTemplate(
            text=u'你好，我是機器人',
            actions=[
                MessageAction(
                    label=u'最新商品',
                    text=u'最新商品'
                ),
                MessageAction(
                    label=u'最新優惠',
                    text=u'最新優惠'
                ),
                MessageAction(
                    label=u'找客服',
                    text=u'找客服'
                )
            ]
        )
    )