import hashlib
import json
import os

import validators
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import ExtractionStrategy

class InvalidUrlError(Exception):
    pass


class UnHashableUrlError(Exception):
    pass


class ProductNotFoundInDatabaseError(Exception):
    pass


class UnableToSaveProductToDatabaseError(Exception):
    pass


class UnableToCrawlProductError(Exception):
    pass


product_data_folder = "products"


class Crawler:
    def __init__(self, url: str):
        self.url = url

    @staticmethod
    def hash_url(url: str) -> str:
        _url = url.split("?")[0].split("#")[0]
        if not validators.url(_url):
            raise InvalidUrlError(f"URL {url} is not valid")

        try:
            return hashlib.md5(_url.encode()).hexdigest()
        except Exception as _:
            raise UnHashableUrlError(f"URL {url} is not hashable")

    @staticmethod
    def _get_product_path(product_hash: str) -> str:
        return f"{product_data_folder}/{product_hash}.json"

    async def save_to_db(product_hash: str, details: list, reviews: list) -> None:
        try:
            with open(Crawler._get_product_path(product_hash=product_hash), "w") as f:
                json.dump(
                    {
                        "details": details[0],
                        "reviews": reviews,
                    },
                    f,
                    indent=4,
                )
        except Exception as e:
            raise UnableToSaveProductToDatabaseError(
                f"Unable to save product with hash {product_hash} to the database : {str(e)}"
            ) from e

    @staticmethod
    def exists_in_db(product_hash: str) -> bool:
        if os.path.exists(Crawler._get_product_path(product_hash=product_hash)):
            return True
        raise ProductNotFoundInDatabaseError(
            f"Product with hash {product_hash} not found"
        )

    @staticmethod
    async def extract(url: str, extraction_strategy: ExtractionStrategy) -> list[dict]:
        async with AsyncWebCrawler(verbose=True, headless=True) as crawler:
            result = await crawler.arun(
                url=url,
                extraction_strategy=extraction_strategy,
                bypass_cache=True,
                verbose=False,
            )
            assert result.success, "Failed to crawl the page"

            return json.loads(result.extracted_content)
