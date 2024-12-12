amazon_product_schema = {
    "name": "Amazon Product Details",
    "baseSelector": "div#centerCol",
    "fields": [
        {
            "name": "title",
            "selector": "span#productTitle",
            "type": "text",
        },
        {
            "name": "price",
            "type": "text",
            "selector": "span#priceblock_ourprice",
        },
        {
            "name": "rating",
            "type": "text",
            "selector": "span.a-icon-alt",
        },
    ],
}
