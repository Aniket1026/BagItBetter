import json
from typing import List
from uuid import uuid4
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from celery.result import AsyncResult
from app.services.crawling_service import (
    app as celery_app,
    extract_and_save_product,
)
from app.db.db import database
from sqlmodel import Session
from app.utils.logging_config import Logger
from app.services.llm_service import llm_service
from app.models.database_schema import JobTracker, Task, JobStatus, CrawledData, LLMTask

logger = Logger().get_logger()


class ProductUrl(BaseModel):
    url: List[str]


router = APIRouter()


@router.post("/enqueue-tasks")
async def compare_product(
    product_urls: List[str], session: Session = Depends(database.get_session)
):

    results = []
    for url in product_urls:
        task_id = str(uuid4())
        try:
            job_tracker = JobTracker(
                id=task_id,
                task_id=task_id,
                task_type=Task.Crawling,
                status=JobStatus.Pending,
            )
            session.add(job_tracker)
            session.commit()

            task = extract_and_save_product.delay(url)
            results.append(
                {
                    "message": "Task enqueued",
                    "task_id": task.id,
                    "url": url,
                    "status": "Pending",
                }
            )
        except Exception as e:
            logger.error(f"Error enqueuing task for URL {url}: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    return {"results": results}




@router.get("/task-status/{task_id}")
async def task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == "SUCCESS":
        return {"status": task_result.state, "result": task_result.result}
    elif task_result.state == "FAILURE":
        return {"status": task_result.state, "error": str(task_result.info)}
    else:
        return {"status": task_result.state}


@router.post("/recommendation")
async def generate_advice(products_info: List[dict]):
    try:
        logger.info(f"Generating recommendation for products: {products_info}")
        response = llm_service.generate_response(products_info)
        return {"response": response}
    except Exception as e:
        logger.error(f"Error generating advice: {str(e)}")
        return {"error": str(e)}
    

    
# @router.post("/enqueue-tasks")
# async def compare_product(
#     product_url: List[str], session: Session = Depends(Database.get_session)
# ):
#     product_meta_data = []
#     result = []
#     print("product_urls : ", product_url)
#     for url in product_url:
#         # try:
#         #     product_hash = ProductDataManager.hash_url(url)
#         # except Exception as e:
#         #     raise HTTPException(status_code=400, detail=str(e))

#         try:
#             await session.exec(
#                 "UPDATE JobTracker SET status = 'pending' WHERE url = :url",
#                 {"url": url},
#             )
#             await session.exec(
#                 "UPDATE JOB SET task = 'crawling' WHERE url = :url", {"url": url}
#             )
#             product_info = await session.exec(
#                 "SELECT data FROM JOB WHERE url = :url", {"url": url}
#             )
#             if product_info:
#                 logger.info(f"Product already exists in the database .......")
#                 await session.exec(
#                     "UPDATE JOB SET status = 'completed' WHERE url = :url", {"url": url}
#                 )
#                 product_meta_data.append(product_info)

#         except Exception as e:
#             await session.exec(
#                 "UPDATE JOB SET status = 'error' WHERE url = :url", {"url": url}
#             )
#             logger.error(f"Product does not exist in the database {str(e)}")
#             raise HTTPException(status_code=400, detail=str(e))

#         try:
# task = extract_and_save_product.delay(url)
#             session.exec(
#                 "INSERT INTO JOB (id,task_type) VALUES (:id,:task_type)",
#                 {"id": url, "task_type": "crawling"},
#             )
#             result.append(
#                 {
#                     "url": url,
#                     "status": "Task enqueued",
#                     "task_id": task.id,
#                 }
#             )
#         except Exception as e:
#             logger.error(f"Unable to extract product details : {str(e)}")
#             raise HTTPException(status_code=400, detail=str(e))

#     return {"message": "Tasks enqueued", "results": result}
