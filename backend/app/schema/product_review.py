amazon_product_reviews_schema = {
    "name": "Amazon Product Reviews",
    "baseSelector": "div.a-section.review.aok-relative",
    "fields": [
        {
            "name": "title",
            "type": "text",
            "selector": "div.a-row>a.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold>span:nth-child(3)",
        },
        {
            "name": "rating",
            "type": "text",
            "selector": "div.a-row>a.a-size-base.a-link-normal.review-title.a-color-base.review-title-content.a-text-bold>i.review-rating>span.a-icon-alt",
        },
        {
            "name": "text",
            "type": "text",
            "selector": "div.a-expander-content.reviewText.review-text-content.a-expander-partial-collapse-content>span",
        },
    ],
}
