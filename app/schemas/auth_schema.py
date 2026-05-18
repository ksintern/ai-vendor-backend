from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr
)


# -----------------------------
# LOGIN REQUEST
# -----------------------------

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# REGISTER REQUEST
# -----------------------------

class RegisterRequest(BaseModel):

    full_name: str

    email: EmailStr

    phone_number: str | None = None

    password: str

    confirm_password: str


# -----------------------------
# USER RESPONSE
# -----------------------------

class UserResponse(BaseModel):

    user_id: UUID

    full_name: str

    email: EmailStr

    phone_number: str | None = None


# -----------------------------
# LOGIN RESPONSE
# -----------------------------

class LoginResponse(BaseModel):

    success: bool

    message: str

    access_token: str | None = None

    token_type: str | None = None

    user: UserResponse


# -----------------------------
# REGISTER RESPONSE
# -----------------------------

class RegisterResponse(BaseModel):

    success: bool

    message: str

    user: UserResponse