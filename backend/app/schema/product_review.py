amazon_product_reviews_schema = {
    "name": "Amazon Product Reviews",
    "baseSelector": "div.a-section.reviews-content",
    "fields": [
        {
            "name": "reviews",
            "type": "list",
            "selector": "div.a-section.celwidget",
            "fields": [
                {
                    "name": "rating",
                    "type": "text",
                    "selector": "div:nth-of-type(2)>h5>a>i",
                },
                {
                    "name": "title",
                    "type": "text",
                    "selector": "div:nth-of-type(2)>h5>a>span:nth-child(3)",
                },
                {
                    "name": "text",
                    "type": "text",
                    "selector": "div:nth-of-type(4)",
                },
            ],
        },
    ],
}