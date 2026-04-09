import asyncio
import os
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from app.schema.product_schema import amazon_product_schema
from app.schema.product_review import amazon_product_reviews_schema
from app.utils.celery_client import CeleryClient
from app.services.amazon_product_extractor import ProductDataManager, InvalidUrlError
from app.db.db import Database
from fastapi import Depends
from sqlmodel import Session

app = CeleryClient.get_app(
    "crawler", os.getenv("BROKER_URL"), os.getenv("BACKEND_URL")
)


@app.task
def extract_and_save_product(url: str, session: Session = Depends(Database.get_session)):
    try:
        product_hash = ProductDataManager.hash_url(url)

        product_info = asyncio.run(ProductDataManager.extract(
            url, JsonCssExtractionStrategy(amazon_product_schema)
        ))
        product_reviews = asyncio.run(ProductDataManager.extract(
            url, JsonCssExtractionStrategy(amazon_product_reviews_schema)
        ))

        asyncio.run(ProductDataManager.save_to_db(
            product_hash,
            details=product_info,
            reviews=product_reviews,
        ))

        return {
            "product_info": product_info,
            "product_reviews": product_reviews,
        }
    except InvalidUrlError as e:
        return {"error": str(e), "status": "failed"}
    except ValueError as e:
        return {"error": f"Invalid data: {str(e)}", "status": "failed"}
    except Exception as e:
        return {"error": f"Failed to process URL: {str(e)}", "status": "failed"}
