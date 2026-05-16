from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.auth_schema import (
    LoginResponse,
    UserResponse
)

from app.core.security import (
    verify_password,
    create_access_token
)


def login_user(
    email: str,
    password: str,
    db: Session
) -> LoginResponse:

    # Find user by email
    user = db.query(User).filter(
        User.email == email
    ).first()

    # User not found
    if not user:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User does not exist"
        )

    # Verify password
    is_valid_password = verify_password(
        password,
        str(user.password_hash)
    )

    # Invalid credentials
    if not is_valid_password:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Inactive account check
    if not bool(user.is_active):

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    # Generate JWT token
    access_token = create_access_token(
        data={
            "sub": str(user.email),
            "user_id": str(user.user_id)
        }
    )

    print(
        "Login successful for:",
        str(user.email)
    )

    return LoginResponse(
        success=True,
        message="Login successful",

        # Real JWT token
        access_token=access_token,
        token_type="bearer",

        user=UserResponse(
            user_id=UUID(str(user.user_id)),
            full_name=str(user.full_name),
            email=str(user.email),

            phone_number=str(user.phone_number)
            if user.phone_number is not None
            else None
        )
    )