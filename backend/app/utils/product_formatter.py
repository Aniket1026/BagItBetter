
def format_product_data(product_data: list) -> str:
    formatted_products = []
    for product in product_data:
        details = product["details"]
        reviews = product.get("reviews", [{}])[0].get("reviews", [])
        formatted_product = f"""
            Title: {details['title']}
            Price: {details['currency']}{details['price']}
            Rating: {details['rating']}

            Reviews:
            """
    for review in reviews[:3]:
        formatted_product += f"- {review['title']}: {review['text']}\n"
    formatted_products.append(formatted_product.strip())

    return "\n\n".join(formatted_products)
