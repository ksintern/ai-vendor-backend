from pydantic import BaseModel, EmailStr
from uuid import UUID


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    user_id: UUID
    full_name: str
    email: EmailStr
    phone_number: str | None = None


class LoginResponse(BaseModel):
    success: bool
    message: str
    access_token: str | None = None
    token_type: str | None = None
    user: UserResponse