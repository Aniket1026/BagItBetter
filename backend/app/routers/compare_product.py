import json
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.services.amazon_product_extractor import ProductDataManager
from app.services.crawling_service import (
    app as celery_app,
    extract_and_save_product,
)
from app.services.llm_service import LLMService

class ProductUrl(BaseModel):
    url: List[str]


router = APIRouter()


@router.post("/enqueue-tasks")
async def compare_product(product_url: List[str]):
    result = []
    print("product_urls : ", product_url)
    for url in product_url:
        try:
            product_hash = ProductDataManager.hash_url(url)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

        try:
            await ProductDataManager.exists_in_db(product_hash)
            print(
                f"Product already exists in the database {ProductDataManager._get_product_path(product_hash)}"
            )
            with open(ProductDataManager._get_product_path(product_hash), "r") as f:
                result.append(json.load(f))
            return result
        except Exception as e:
            print("Product not found in the database , crawling the product......")

        try:
            task = extract_and_save_product.delay(url, product_hash)
            result.append(
                {
                    "url": url,
                    "status": "Task enqueued",
                    "task_id": task.id,
                }
            )
        except Exception as e:
            print("Unable to extract product details : ", e)
            raise HTTPException(status_code=400, detail=str(e))

    return {"message": "Tasks enqueued", "results": result}


@router.get("/task-status/{task_id}")
async def task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == "SUCCESS":
        return {"status": task_result.state, "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": task_result.state, "error": str(task_result.info)}
    else:
        return {"status": task_result.state}


@router.post("/products/compare-and-recommend")
async def generate_advice(products_info: List[dict]):
    llm_service = LLMService()
    try:
        response = llm_service.generate_response(products_info)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
