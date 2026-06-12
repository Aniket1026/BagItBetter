from sqlmodel import SQLModel, Field, Index, Relationship
from uuid import UUID, uuid4
from enum import Enum
from typing import Optional
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import ENUM as PGEnum
from sqlalchemy import Column as COLUMN


class Task(str, Enum):
    Unknown = "Unknown"
    Crawling = "Crawling"
    Recommending = "Recommending"


class JobStatus(str, Enum):
    Pending = "Pending"
    Error = "Error"
    Completed = "Completed"


class User(SQLModel, table=True):
    id: UUID = Field(default=uuid4(), primary_key=True)
    name: Optional[str] = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)

    crawled_data: list["CrawledData"] = Relationship(back_populates="user")
    recommendations: list["LLMTask"] = Relationship(back_populates="user")


class CrawledData(SQLModel, table=True):
    id: UUID = Field(default=uuid4(), primary_key=True)
    url: str = Field(default=None)
    product_info: dict = Field(default={}, sa_column=COLUMN(JSONB))
    product_reviews: dict = Field(default={}, sa_column=COLUMN(JSONB))

    user_id: UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="crawled_data")


class LLMTask(SQLModel, table=True):
    id: UUID = Field(default=uuid4(), primary_key=True)
    status: JobStatus = Field(
        sa_column=COLUMN(
            PGEnum(JobStatus, name="jobstatus", create_type=True),
            nullable=False,
            server_default=JobStatus.Pending.value,
        )
    )
    task_type: Task = Field(
        sa_column=COLUMN(
            PGEnum(Task, name="task", create_type=True),
            nullable=False,
            server_default=Task.Unknown.value,
        )
    )

    data: str = Field(default="")

    user_id: UUID = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="recommendations")

    class Config:
        table_args = Index("index_id_status", "id", "status")


class JobTracker(SQLModel, table=True):
    id: UUID = Field(default=uuid4(), primary_key=True)
    task_id: str = Field(default="")
    task_type: Task = Field(
        sa_column=COLUMN(
            PGEnum(Task, name="task", create_type=True),
            nullable=False,
            server_default=Task.Unknown.value,
        )
    )
    status: JobStatus = Field(
        sa_column=COLUMN(
            PGEnum(JobStatus, name="jobstatus", create_type=True),
            nullable=False,
            server_default=JobStatus.Pending.value,
        )
    )
    data: Optional[str] = Field(default="")
    error_message: Optional[str] = Field(default=None)

    class Config:
        table_args = Index("index_id_status", "id", "status")
