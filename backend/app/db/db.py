import os
import logging
from typing import Generator

from sqlmodel import Session, create_engine

# -------------------------------------------------
# Logging
# -------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# -------------------------------------------------
# Database Configuration
# -------------------------------------------------
class DatabaseConfig:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER", "postgres")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")

        if not all([self.host, self.port, self.user, self.password, self.database]):
            raise ValueError(
                "Missing required environment variables for database connection."
            )

    @property
    def url(self) -> str:
        return (
            f"postgresql://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}"
        )


config = DatabaseConfig()

engine = create_engine(
    config.url,
    echo=False,  # Set True if we want SQL logs
    pool_pre_ping=True,  # Prevent stale connections
)


# -------------------------------------------------
# Database Dependency
# -------------------------------------------------
class Database:
    def get_session(self) -> Generator[Session, None, None]:
        try:
            with Session(engine) as session:
                yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            raise


# -------------------------------------------------
# Single shared instance
# -------------------------------------------------
database = Database()
