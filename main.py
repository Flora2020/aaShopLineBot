import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TemplateSendMessage, ButtonsTemplate
)
from linebot.models.actions import (
    PostbackAction, MessageAction, URIAction
)

from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))


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
def send_menu(event):
    trigger = '開始查詢'

    if event.message.text.find(trigger) == -1:
        return

    buttons_template_message = TemplateSendMessage(
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

    line_bot_api.reply_message(
        event.reply_token,
        buttons_template_message
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
