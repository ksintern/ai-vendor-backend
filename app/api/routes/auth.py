from fastapi import (
    APIRouter,
    Depends
)

from fastapi.security import (
    OAuth2PasswordRequestForm
)

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
        username=request.username,
        full_name=request.full_name,
        email=request.email,
        phone_number=request.phone_number,
        password=request.password,
        confirm_password=request.confirm_password,
        db=db
    )


# -----------------------------
# FRONTEND LOGIN API
# JSON-BASED LOGIN
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
        identifier=request.identifier,
        password=request.password,
        db=db
    )


# -----------------------------
# SWAGGER / OAUTH LOGIN
# FORM-DATA LOGIN
# -----------------------------

@router.post(
    "/token",
    response_model=LoginResponse
)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    return login_user(
        identifier=form_data.username,
        password=form_data.password,
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
            "username": current_user.username,
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