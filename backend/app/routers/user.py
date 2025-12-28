from fastapi import APIRouter, HTTPException, Depends, Response, Request
from sqlmodel import Session,select
from app.db.db import database
from app.utils.logging_config import Logger
from app.schema.user import UserRegister, UserLogin
from app.utils.security import Security
from app.db.session_manager import SessionManager
from app.models.database_schema import User


logger = Logger().get_logger()
router = APIRouter()


@router.post("/register")
def register(
    user: UserRegister, response: Response, db: Session = Depends(database.get_session)
):
    try:
        print(" user", user)
        existing_user = db.exec(select(User).where(User.email == user.email)).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")

        hashed_password = Security.get_password_hash(user.password)
        user.password = hashed_password

        new_user = User(
            name=user.name,
            email=user.email,
            password=user.password,
            crawled_data=[],
            recommendations=[],
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = SessionManager.create_session_token(new_user.id)
        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            samesite="Lax",
            secure=True,
            max_age=3600,
            expires=3600,
        )

        user_data = {"name": new_user.name, "email": new_user.email}
        return {"message": "Registration successful", "data": user_data}

    except Exception as e:
        logger.error(f"Error in register: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/login")
async def login(
    user: UserLogin, response: Response, db: Session = Depends(database.get_session)
):
    try:
        existing_user = db.exec(select(User).where(User.email == user.email)).first()
        if not existing_user:
            raise HTTPException(status_code=400, detail="User not found")

        if not Security.verify_password(user.password, existing_user.password):
            raise HTTPException(status_code=400, detail="Invalid credentials")

        token = SessionManager.create_session_token(existing_user.id)
        user_data = {"name": existing_user.name, "email": existing_user.email}

        response.set_cookie(
            key="session_token",
            value=token,
            httponly=True,
            samesite="Lax",
            secure=True,
            max_age=3600,
            expires=3600,
        )

    except Exception as e:
        logger.error(f"Error in login: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"message": "Login successful", "data": user_data}


@router.post("/logout")
async def logout(request: Request, response: Response):
    try:
        token = request.cookies.get("session_token")
        if not token:
            logger.error("No token found")
            raise HTTPException(status_code=400, detail="Invalid token")

        if SessionManager.is_valid_session(token) is False:
            logger.error("Invalid token")
            raise HTTPException(status_code=400, detail="Invalid token")

        response.delete_cookie("session_token")
        if token in SessionManager.session_store:
            del SessionManager.session_store[token]

        return {"message": "Logout successful"}
    except Exception as e:
        logger.error(f"Error in logout: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
