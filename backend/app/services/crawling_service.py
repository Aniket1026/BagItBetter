import asyncio
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from app.schema.product_schema import amazon_product_schema
from app.schema.product_review import amazon_product_reviews_schema
from app.utils.celery_client import CeleryClient
from app.services.amazon_product_extractor import ProductDataManager

app = CeleryClient.get_app(
    "crawler", "redis://localhost:6379/0", "redis://localhost:6379/0"
)


@app.task
def extract_and_save_product(url: str, product_hash: str):
    async def crawl_and_save():
        product_info = await ProductDataManager.extract(
            url, JsonCssExtractionStrategy(amazon_product_schema)
        )
        product_reviews = await ProductDataManager.extract(
            url, JsonCssExtractionStrategy(amazon_product_reviews_schema)
        )

        await ProductDataManager.save_to_db(
            product_hash=product_hash,
            details=product_info,
            reviews=product_reviews,
        )

        return {
            "product_info": product_info,
            "product_reviews": product_reviews,
        }

    return asyncio.run(crawl_and_save())
