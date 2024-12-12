from app.routers.compare_product import router
from fastapi import FastAPI
import uvicorn

app = FastAPI()
origins = ["*"]

app.include_router(router, prefix="/api/v1", tags=["compare-product"])


@app.get("/")
async def root():
    return {"message": "Hello World new update"}


if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=8000, reload=True)
