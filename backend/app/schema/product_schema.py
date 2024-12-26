amazon_product_schema = {
    "name": "Amazon Product Details",
    "baseSelector": "div#centerCol",
    "fields": [
        {
            "name": "title",
            "type": "text",
            "selector": "span#productTitle",
        },
        {
            "name": "currency",
            "type": "text",
            "selector": "div.a-section>span.a-price>span>span.a-price-symbol",
        },
        {
            "name": "price",
            "type": "text",
            "selector": "div.a-section>span.a-price>span>span.a-price-whole",
        },
        {
            "name": "rating",
            "type": "text",
            "selector": "span.a-icon-alt",
        },
    ],
}