from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from api.schemas import BasicResponse
from api.schemas.user import *
from api.services.user_service import UserService
from db.session import get_db
from core.status_code import StatusCode

router = APIRouter(tags=["user"])
user_service = UserService

@router.post(path="/login", response_model=LoginResponse)
async def login_user(login: LoginRequest, request: Request, db: Session = Depends(get_db)):
    ip_address = request.client.host
    try:
        result = await user_service.login_user(db, login, ip_address)
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

    if result == "MUST_HAVE_ENTER_ACCOUNT":
        return JSONResponse(
            content=StatusCode.CODE4305.response(),
            status_code=400
        )
    elif result == "MUST_HAVE_ENTER_PASSWORD":
        return JSONResponse(
            content=StatusCode.CODE4306.response(),
            status_code=400
        )
    elif result == "USER_NOT_FOUND":
        return JSONResponse(
            content=StatusCode.CODE4101.response(),
            status_code=400
        )
    elif result == "INVALID_PASSWORD":
        return JSONResponse(
            content=StatusCode.CODE4401.response(),
            status_code=400
        )
    return JSONResponse(
        content=result.dict(),
        status_code=200
    )


@router.post("/logout", response_model=BasicResponse)
async def logout_user(logout: LogoutRequest, request: Request, db: Session = Depends(get_db)):
    ip_address = request.client.host


@router.post(path="/users", response_model=BasicResponse)
async def create_user(request: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        result = await user_service.create_user(db, request)
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

    if result == "ALREADY_EXISTS":
        return JSONResponse(
            content=StatusCode.CODE4201.response(),
            status_code=400
        )
    elif result == "INVALID_ACCOUNT_LEN":
        return JSONResponse(
            content=StatusCode.CODE4301.response(),
            status_code=400
        )
    elif result == "ACCOUNT_CONTAINS_BLANK":
        return JSONResponse(
            content=StatusCode.CODE4302.response(),
            status_code=400
        )
    elif result == "INVALID_PASSWORD_FORMAT":
        return JSONResponse(
            content=StatusCode.CODE4303.response(),
            status_code=400
        )
    elif result == "INVALID_EMAIL":
        return JSONResponse(
            content=StatusCode.CODE4304.response(),
            status_code=400
        )
    return JSONResponse(
        content=result.dict(),
        status_code=200
    )


user_router = router