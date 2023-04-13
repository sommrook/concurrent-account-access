from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from api.schemas.user import LoginResponse, LoginRequest
from api.services.user_service import UserService
from db.session import get_db
from core.status_code import StatusCode

router = APIRouter(tags=["user"])
user_service = UserService

@router.post(path="/login", response_model=LoginResponse)
async def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        pass
    except SQLAlchemyError as e:
        print(e)
        db.rollback()
        return JSONResponse(
            content=StatusCode.CODE5001.response(),
            status_code=500
        )
    except Exception as e:
        print(e)
        db.rollback()
        return JSONResponse(
            content=StatusCode.CODE5000.response(),
            status_code=500
        )
    finally:
        db.close()

user_router = router