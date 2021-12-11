import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage
)

from dotenv import load_dotenv
from chat_flow_helper import menu_helper

app = Flask(__name__)

load_dotenv()
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

# record session status
wait_for_reply = {
    'asked_name': set()  # collect users who is asked name
}


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
def menu(event):
    trigger = {
        'query': '開始查詢',
        'menu': '主選單',
        'new_arrival': '最新商品',
        'new_offer': '最新優惠',
        'customer_service': '客服'
    }
    message = None

    if event.message.text.find(trigger['query']) != -1 \
            or event.message.text.find(trigger['menu']) != -1:
        message = menu_helper.get_menu()

    if event.message.text.find(trigger['new_arrival']) != -1:
        message = menu_helper.get_new_arrivals()

    if event.message.text.find(trigger['new_offer']) != -1:
        message = menu_helper.get_new_offer()

    user_id = event.source.user_id
    if event.message.text.find(trigger['customer_service']) != -1:
        message = menu_helper.ask_user_name()
        wait_for_reply['asked_name'].add(user_id)
    elif user_id in wait_for_reply['asked_name']:
        message = menu_helper.get_customer_service(event.message.text)
        wait_for_reply['asked_name'].discard(user_id)

    if message is None:
        message = menu_helper.get_default_message()

    line_bot_api.reply_message(
        event.reply_token,
        message
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
