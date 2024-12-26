import os
from langchain_openai import OpenAI

class LLMService:
    def __init__(self):
        self.llm = OpenAI(
            model="gpt-3.5-turbo-instruct",
            temperature=0,
            max_retries=2,
            api_key=os.getenv("OPEN_API_KEY"),
        )

    def format_product_data(self, product_data: list) -> str:
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

    def generate_response(self,product_data) -> str:
        formatted_product_data = self.format_product_data(product_data)
        formatted_prompt = f"""
            You are a advisor for customers who are planning to buy a product from an ecommerce site.
            The customers are confused between the various products.
            The customers want to compare the products based on their features, price, ratings, and user reviews.
            Compare the following products based on their features:
            {formatted_product_data}

            Provide a detailed analysis covering:
            - Price
            - Ratings
            - User Reviews

            Conclude with the most suitable choice for customers. 
            Reason out why the chosen product is the best option for the customers.                                                                           
                                                    
            """
        return self.llm.invoke(formatted_prompt)
