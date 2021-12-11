from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, CarouselTemplate, CarouselColumn,
    ImageSendMessage, TextSendMessage, QuickReply, QuickReplyButton
)
from linebot.models.actions import (
    MessageAction, URIAction
)


def get_default_message():
    return TemplateSendMessage(
        alt_text=u'開始查詢',
        template=ButtonsTemplate(
            text=u'你好，請點擊「開始查詢」以取得主選單',
            actions=[
                MessageAction(
                    label=u'開始查詢',
                    text=u'開始查詢'
                )
            ]
        )
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


def get_new_arrivals():
    new_arrivals = [
        {
            'name': u'商品1',
            'image_url': 'https://loremflickr.com/320/240?lock=3861',
            'price': 44920,
            'product_url': 'http://34.80.108.187/products/1'
        },
        {
            'name': u'商品2',
            'image_url': 'https://loremflickr.com/320/240?lock=5344',
            'price': 11860,
            'product_url': 'http://34.80.108.187/products/2'
        },
        {
            'name': u'商品3',
            'image_url': 'https://loremflickr.com/320/240?lock=5594',
            'price': 27369,
            'product_url': 'http://34.80.108.187/products/3'
        }
    ]

    columns = []
    for product in new_arrivals:
        columns.append(
            CarouselColumn(
                thumbnail_image_url=product['image_url'],
                title=product['name'],
                text=f'TWD$ {product["price"]:,}',
                actions=[
                    URIAction(
                        label=u'查看商品',
                        uri=product['product_url']
                    ),
                    MessageAction(
                        label=u'回主選單',
                        text=u'回主選單'
                    ),
                ]
            )
        )

    return TemplateSendMessage(
        alt_text=u'最新商品',
        template=CarouselTemplate(
            columns=columns
        )
    )


def get_new_offer():
    offer = {
        'original_content_url': 'https://loremflickr.com/320/240?lock=8280',
        'preview_image_url': 'https://loremflickr.com/320/240?lock=8280',
        'product_name': u'商品10',
        'product_url': 'http://34.80.108.187/products/10'
    }

    return [
        ImageSendMessage(
            original_content_url=offer['original_content_url'],
            preview_image_url=offer['preview_image_url']
        ),
        TemplateSendMessage(
            alt_text=u'最新優惠',
            template=ButtonsTemplate(
                text=offer['product_name'],
                actions=[
                    URIAction(
                        label=u'查看優惠',
                        uri=offer['product_url']
                    ),
                    MessageAction(
                        label=u'回主選單',
                        text=u'回主選單'
                    ),
                ]
            )
        )
    ]


def ask_user_name():
    return TextSendMessage(text=u'你好，請問怎樣稱呼？')


def get_customer_service(name):
    return TextSendMessage(
        text=f'你好 {name}，請問你想查詢什麼？',
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label=u'會員積分', text=u'會員積分')),
                QuickReplyButton(action=MessageAction(label=u'退/換貨', text=u'退/換貨')),
                QuickReplyButton(action=MessageAction(label=u'點錯了', text=u'點錯了')),
            ]
        ))
