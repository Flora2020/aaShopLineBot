from linebot.models import (
    TemplateSendMessage, ButtonsTemplate, CarouselTemplate, CarouselColumn,
    ImageSendMessage, TextSendMessage, QuickReply, QuickReplyButton
)
from linebot.models.actions import (
    MessageAction, URIAction
)

from constants.menu import TRIGGERS, ACTIONS, TEMPLATES, CUSTOMER_SERVICE_CHAT


def get_default_message():
    return TemplateSendMessage(
        alt_text=TRIGGERS['query'],
        template=ButtonsTemplate(
            text=TEMPLATES['get_menu'],
            actions=[
                MessageAction(
                    label=TRIGGERS['query'],
                    text=TRIGGERS['query']
                )
            ]
        )
    )


def get_menu():
    return TemplateSendMessage(
        alt_text=TRIGGERS['menu'],
        template=ButtonsTemplate(
            text=TEMPLATES['greeting'],
            actions=[
                MessageAction(
                    label=TRIGGERS['new_arrival'],
                    text=TRIGGERS['new_arrival']
                ),
                MessageAction(
                    label=TRIGGERS['new_offer'],
                    text=TRIGGERS['new_offer']
                ),
                MessageAction(
                    label=ACTIONS['find_customer_service'],
                    text=ACTIONS['find_customer_service']
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
                text=f'TWD${product["price"]:,}',
                actions=[
                    URIAction(
                        label=ACTIONS['view_product_detail'],
                        uri=product['product_url']
                    ),
                    MessageAction(
                        label=ACTIONS['back_to_menu'],
                        text=ACTIONS['back_to_menu']
                    ),
                ],
                default_action=URIAction(
                    uri=product['product_url']
                )
            )
        )

    return TemplateSendMessage(
        alt_text=TRIGGERS['new_arrival'],
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
            alt_text=TRIGGERS['new_offer'],
            template=ButtonsTemplate(
                text=offer['product_name'],
                actions=[
                    URIAction(
                        label=ACTIONS['view_product_offer'],
                        uri=offer['product_url']
                    ),
                    MessageAction(
                        label=ACTIONS['back_to_menu'],
                        text=ACTIONS['back_to_menu']
                    ),
                ]
            )
        )
    ]


def ask_user_name():
    return TextSendMessage(text=CUSTOMER_SERVICE_CHAT['ask_name'])


def get_customer_service(name):
    return TextSendMessage(
        text=CUSTOMER_SERVICE_CHAT['greeting'](name),
        quick_reply=QuickReply(
            items=[
                QuickReplyButton(
                    action=MessageAction(
                        label=TRIGGERS['loyalty_point'],
                        text=TRIGGERS['loyalty_point']
                    )
                ),
                QuickReplyButton(
                    action=MessageAction(
                        label=TRIGGERS['return_or_exchange'],
                        text=TRIGGERS['return_or_exchange']
                    )
                ),
                QuickReplyButton(
                    action=MessageAction(
                        label=TRIGGERS['fat_finger'],
                        text=TRIGGERS['fat_finger']
                    )
                ),
            ]
        ))


def get_query_reply():
    return TextSendMessage(text=CUSTOMER_SERVICE_CHAT['contact_you_soon'])
