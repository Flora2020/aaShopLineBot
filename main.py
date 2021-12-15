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


def create_app():
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
        """
        chat flow
        trigger: 開始查詢、主選單、點錯了 --> 提供選項：最新商品、最新優惠、找客服
        trigger: 最新商品 --> 提供資訊：商品圖片、商品名稱、商品價格、商品購買網址、回主選單
        trigger: 最新優惠 --> 提供資訊：優惠商品圖片、優惠商品名稱、優惠商品購買網址、回主選單
        trigger: 客服 --> 詢問稱呼 --> 提供選項：會員積分、退/換貨、點錯了
        trigger: 會員積分、退/換貨 -->  回覆：客服會很快聯繫你
        """

        user_message = event.message.text
        user_id = event.source.user_id

        if user_message.find(TRIGGERS['query']) != -1 \
                or user_message.find(TRIGGERS['menu']) != -1 \
                or user_message.find(TRIGGERS['fat_finger']) != -1:
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

        elif user_message.find(TRIGGERS['loyalty_point']) != -1 \
                or user_message.find(TRIGGERS['return_or_exchange']) != -1:
            message = menu_helper.get_query_reply()

        else:
            message = menu_helper.get_default_message()

        line_bot_api.reply_message(
            event.reply_token,
            message
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=5000, debug=True)
