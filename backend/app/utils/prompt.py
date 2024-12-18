from langchain_core.prompts import PromptTemplate

template = """
   You are a advisor for customers who are planning to buy a product from an ecommerce site.
The customers are confused between the various products.
The customers want to compare the products based on their features, price, ratings, and user reviews.
Compare the following products based on their features:
{product_data}

Provide a detailed analysis covering:
- Price
- Ratings
- User Reviews

Conclude with the most suitable choice for customers. 
Reason out why the chosen product is the best option for the customers.                                                                           
                                           
"""

prompt = PromptTemplate(
    input_variables=["product_data"],
    template=template,
)
