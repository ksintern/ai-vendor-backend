from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse
)

from app.services.auth_service import login_user

from app.db.session import get_db

from app.api.dependencies.auth_dependency import (
    get_current_user
)

from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# -----------------------------
# LOGIN API
# -----------------------------

@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    return login_user(
        email=request.email,
        password=request.password,
        db=db
    )


# -----------------------------
# PROTECTED USER API
# -----------------------------

@router.get("/me")
def get_logged_in_user(

    current_user: User = Depends(
        get_current_user
    )
):

    return {
        "success": True,
        "message": "Authenticated user fetched successfully",

        "user": {
            "user_id": str(current_user.user_id),
            "full_name": current_user.full_name,
            "email": current_user.email,
            "phone_number": current_user.phone_number
        }
    }