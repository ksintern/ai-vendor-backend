from uuid import UUID

from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.auth_schema import (
    LoginResponse,
    RegisterResponse,
    UserResponse
)

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token
)


# -----------------------------
# REGISTER USER
# -----------------------------

def register_user(
    full_name: str,
    email: str,
    phone_number: str | None,
    password: str,
    confirm_password: str,
    db: Session
) -> RegisterResponse:

    # Check existing user
    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Password confirmation check
    if password != confirm_password:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # Hash password
    hashed_password = hash_password(password)

    # Create new user
    new_user = User(
        full_name=full_name,
        email=email,
        phone_number=phone_number,

        # Default RBAC-ready role
        role="user",

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
            full_name=str(new_user.full_name),
            email=str(new_user.email),

            phone_number=str(new_user.phone_number)
            if new_user.phone_number is not None
            else None
        )
    )


# -----------------------------
# LOGIN USER
# -----------------------------

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
            "user_id": str(user.user_id),

            # RBAC-ready token payload
            "role": str(user.role)
        }
    )

    print(
        "Login successful for:",
        str(user.email)
    )

    return LoginResponse(
        success=True,
        message="Login successful",

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