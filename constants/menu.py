TRIGGERS = {
    'query': u'開始查詢',
    'menu': u'主選單',
    'new_arrival': u'最新商品',
    'new_offer': u'最新優惠',
    'customer_service': u'客服',
    'loyalty_point': u'會員積分',
    'return_or_exchange': u'退/換貨',
    'fat_finger': u'點錯了'
}

ACTIONS = {
    'find_customer_service': u'找' + TRIGGERS['customer_service'],
    'back_to_menu': u'回' + TRIGGERS['menu'],
    'view_product_detail': u'查看商品',
    'view_product_offer': u'查看優惠'
}

TEMPLATES = {
    'get_menu': f'你好，請點擊「{TRIGGERS["query"]}」以取得{TRIGGERS["menu"]}',
    'greeting': u'你好，我是機器人',
}

CUSTOMER_SERVICE_CHAT = {
    'ask_name': u'你好，請問怎樣稱呼？',
    'greeting': lambda name: f'你好 {name}，請問你想查詢甚麼？',
    'contact_you_soon': '謝謝你！我們的客服人員會很快聯絡你',
}
