from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.schemas.auth_schema import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RegisterResponse
)

from app.services.auth_service import (
    login_user,
    register_user
)

from app.db.session import get_db

from app.api.dependencies.auth_dependency import (
    get_current_user,
    require_role
)

from app.models.user import User


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# -----------------------------
# REGISTER API
# -----------------------------

@router.post(
    "/register",
    response_model=RegisterResponse
)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):

    return register_user(
        full_name=request.full_name,
        email=request.email,
        phone_number=request.phone_number,
        password=request.password,
        confirm_password=request.confirm_password,
        db=db
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
# CURRENT AUTHENTICATED USER
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
            "phone_number": current_user.phone_number,
            "role": current_user.role
        }
    }


# -----------------------------
# ADMIN ONLY ROUTE
# -----------------------------

@router.get("/admin-only")
def admin_only_route(

    current_user: User = Depends(
        require_role(["admin"])
    )
):

    return {
        "success": True,
        "message": "Welcome Admin",

        "user": {
            "email": current_user.email,
            "role": current_user.role
        }
    }


# -----------------------------
# USER ONLY ROUTE
# -----------------------------

@router.get("/user-only")
def user_only_route(

    current_user: User = Depends(
        require_role(["user"])
    )
):

    return {
        "success": True,
        "message": "Welcome User",

        "user": {
            "email": current_user.email,
            "role": current_user.role
        }
    }