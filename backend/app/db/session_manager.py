import time
import uuid
from fastapi import HTTPException
from app.utils.logging_config import Logger

logger = Logger().get_logger()


class SessionManager:
    session_expires = 3600
    session_store = {}

    @classmethod
    def create_session_token(cls, user_id: int) -> str:
        try:
            session_id = str(uuid.uuid4())
            session_expire = time.time() + cls.session_expires
            cls.session_store[session_id] = {
                "user_id": user_id,
                "expires": session_expire,
            }
        except Exception as e:
            logger.error(f"Error in create_session_token: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"session token creation failed: {str(e)}"
            )
        return session_id

    @classmethod
    def is_valid_session(cls, session_id: str) -> bool:
        try:
            if session_id not in cls.session_store:
                return False
            if cls.session_store[session_id]["expires"] < time.time():
                cls.session_store.pop(session_id)
                return False
            return True
        except Exception as e:
            logger.error(f"Error in is_valid_session: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"session token validation failed: {str(e)}"
            )

    @classmethod
    def get_user_id(cls, session_id: str) -> int:
        try:
            if not cls.is_valid_session(session_id):
                return None
            return cls.session_store[session_id]["user_id"] 
        except Exception as e:
            logger.error(f"Error in get_user_id: {str(e)}")
            raise HTTPException(
                status_code=500, detail=f"session token validation failed: {str(e)}"
            )
