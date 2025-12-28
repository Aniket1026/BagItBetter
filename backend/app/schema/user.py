from sqlmodel import SQLModel, Field


class UserRegister(SQLModel):
    id: int = Field(default=None, primary_key=True)
    name : str = Field(default=None)
    email: str = Field(default=None)
    password: str = Field(default=None)


class UserLogin(SQLModel):
    id: int = Field(default=None, primary_key=True)
    email: str = Field(default=None)
    password: str = Field(default=None)

