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
from constants.menu import TRIGGERS

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
    user_message = event.message.text
    user_id = event.source.user_id

    if user_message.find(TRIGGERS['query']) != -1 \
            or event.message.text.find(TRIGGERS['menu']) != -1:
        message = menu_helper.get_menu()

    elif user_message.find(TRIGGERS['new_arrival']) != -1:
        message = menu_helper.get_new_arrivals()

    elif user_message.find(TRIGGERS['new_offer']) != -1:
        message = menu_helper.get_new_offer()

    elif user_message.find(TRIGGERS['customer_service']) != -1:
        message = menu_helper.ask_user_name()
        wait_for_reply['asked_name'].add(user_id)

    elif user_id in wait_for_reply['asked_name']:
        message = menu_helper.get_customer_service(user_message)
        wait_for_reply['asked_name'].discard(user_id)

    else:
        message = menu_helper.get_default_message()

    line_bot_api.reply_message(
        event.reply_token,
        message
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
