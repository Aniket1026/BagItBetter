from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.database_schema import User
from fastapi import HTTPException
from app.utils.logging_config import Logger
import hashlib

logger = Logger().get_logger()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Security:
    @classmethod
    def _pre_hash(cls, password: str) -> str:
        """
        Normalize and pre-hash password to avoid bcrypt 72-byte limit
        """
        password = password.strip()
        return hashlib.sha256(password.encode("utf-8")).digest()

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        prehashed = cls._pre_hash(password)
        return pwd_context.hash(prehashed)

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        prehashed = cls._pre_hash(plain_password)
        return pwd_context.verify(prehashed, hashed_password)

    @classmethod
    def authenticate_user(cls, db: Session, email: str, password: str) -> User | None:
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return None

            if not cls.verify_password(password, user.password):
                return None

            return user

        except Exception as e:
            logger.error(f"Error in authenticate_user: {str(e)}")
            raise HTTPException(status_code=500, detail="Error authenticating user")
