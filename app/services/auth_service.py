from uuid import UUID

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from sqlalchemy import or_

from app.models.user import User

from app.schemas.auth_schema import (
    LoginResponse,
    RegisterResponse,
    UserResponse
)

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token
)


# -----------------------------
# REGISTER USER
# -----------------------------

def register_user(
    username: str,
    full_name: str,
    email: str,
    business_email: str | None,
    phone_number: str | None,
    role: str,
    password: str,
    confirm_password: str,
    db: Session
) -> RegisterResponse:

    # CHECK EXISTING EMAIL

    existing_email = db.query(User).filter(
        User.email == email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # CHECK EXISTING USERNAME

    existing_username = db.query(User).filter(
        User.username == username
    ).first()

    if existing_username:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )

    # PASSWORD CONFIRMATION CHECK

    if password != confirm_password:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # BUSINESS EMAIL REQUIRED FOR VENDORS

    if role == "vendor" and not business_email:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Business email is required for vendors"
        )

    # HASH PASSWORD

    hashed_password = hash_password(password)

    # CREATE USER

    new_user = User(

        username=username,

        full_name=full_name,

        email=email,

        phone_number=phone_number,

        role=role,

        password_hash=hashed_password
    )

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    print(
        "User registered successfully:",
        str(new_user.email)
    )

    return RegisterResponse(

        success=True,

        message="User registered successfully",

        user=UserResponse(

            user_id=UUID(str(new_user.user_id)),

            username=str(new_user.username),

            full_name=str(new_user.full_name),

            email=str(new_user.email),

            role=str(new_user.role),

            phone_number=str(new_user.phone_number)
            if new_user.phone_number is not None
            else None
        )
    )

# -----------------------------
# LOGIN USER
# -----------------------------

def login_user(
    identifier: str,
    password: str,
    db: Session
):

    # LOGIN USING EMAIL OR USERNAME

    user = db.query(User).filter(

        or_(
            User.email == identifier,
            User.username == identifier
        )

    ).first()

    # USER NOT FOUND

    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    # VERIFY PASSWORD

    is_valid_password = verify_password(
        password,
        str(user.password_hash)
    )

    if not is_valid_password:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # INACTIVE ACCOUNT CHECK

    if not bool(user.is_active):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # GENERATE ACCESS TOKEN

    access_token = create_access_token(

        data={

            "sub": str(user.email),

            "user_id": str(user.user_id),

            "role": str(user.role)
        }
    )

    # GENERATE REFRESH TOKEN

    refresh_token = create_refresh_token(

        data={

            "sub": str(user.email),

            "user_id": str(user.user_id),
            
            "role": str(user.role)
        }
    )

    print(
        "Login successful for:",
        str(user.email)
    )

    return {

        "success": True,

        "message": "Login successful",

        "access_token": access_token,

        "refresh_token": refresh_token,

        "token_type": "bearer",

        "user": {

            "user_id": str(user.user_id),

            "username": str(user.username),

            "full_name": str(user.full_name),

            "email": str(user.email),

            "role": str(user.role),

            "phone_number": str(user.phone_number)
            if user.phone_number is not None
            else None
        }
    }