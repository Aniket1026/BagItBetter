from app.routers.compare_product import router as product_router
from app.routers.user import router as user_router
from app.db.db import database
from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine
from app.utils.logging_config import Logger
from app.db.db import engine, DatabaseConfig
from app.models.database_schema import *
import uvicorn

app = FastAPI()
origins = ["*"]

# Create a synchronous engine for table creation
DATABASE_URL = DatabaseConfig().url
sync_engine = create_engine(DATABASE_URL)


async def connect_to_db():
    SQLModel.metadata.create_all(engine)
    Logger().get_logger().info("Database connection established")

    SQLModel.metadata.create_all(sync_engine)
    Logger().get_logger().info("Tables created")


app.add_event_handler("startup", connect_to_db)
# app.add_event_handler("shutdown", close_db_connection)

app.include_router(product_router, prefix="/api/v1", tags=["compare-product"])
app.include_router(user_router, prefix="/api/v1", tags=["user-route"])

@app.get("/healthcheck")
async def root():
    return {"message": "Server is running fine"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
