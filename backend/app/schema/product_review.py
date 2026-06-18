amazon_product_reviews_schema = {
    "name": "Amazon Product Reviews",
    "baseSelector": "ul#localTopReviewsList",
    "fields": [
        {
            "name": "reviews",
            "type": "list",
            "selector": "div.a-section.aok-relative",
            "fields": [
                {
                    "name": "rating",
                    "type": "text",
                    "selector": "div:nth-of-type(2)>i>span",
                },
                {
                    "name": "title",
                    "type": "text",
                    "selector": "a>h5",
                },
                {
                    "name": "review date",
                    "type": "text",
                    "selector": "div:nth-of-type(3)>span",
                },
                {
                    "name": "purchase verification",
                    "type": "text",
                    "selector": "div:nth-of-type(4)>span",
                },
                {
                    "name": "purchase verification",
                    "type": "text",
                    "selector": "div:nth-of-type(5)>div>div>div>div>div>div>div>div>p>span",
                },
            ],
        },
    ],
}