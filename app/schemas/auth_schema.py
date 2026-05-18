from uuid import UUID

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator
)

import re


# -----------------------------
# LOGIN REQUEST
# -----------------------------

class LoginRequest(BaseModel):

    # Email OR Username

    identifier: str = Field(
        min_length=3,
        max_length=100
    )

    password: str = Field(
        min_length=8,
        max_length=100
    )


# -----------------------------
# REGISTER REQUEST
# -----------------------------

class RegisterRequest(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=30
    )

    full_name: str = Field(
        min_length=2,
        max_length=100
    )

    email: EmailStr

    phone_number: str | None = None

    password: str = Field(
        min_length=8,
        max_length=100
    )

    confirm_password: str


    # -----------------------------
    # USERNAME VALIDATION
    # -----------------------------

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):

        if not re.match(
            r"^[a-zA-Z0-9._-]+$",
            value
        ):

            raise ValueError(
                "Username can only contain letters, numbers, dots, hyphens, and underscores"
            )

        return value


    # -----------------------------
    # PHONE NUMBER VALIDATION
    # -----------------------------

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(
        cls,
        value: str | None
    ):

        if value:

            if not re.match(
                r"^[0-9]{10}$",
                value
            ):

                raise ValueError(
                    "Phone number must contain exactly 10 digits"
                )

        return value


    # -----------------------------
    # PASSWORD VALIDATION
    # -----------------------------

    @field_validator("password")
    @classmethod
    def validate_password(
        cls,
        value: str
    ):

        if not re.search(r"[A-Z]", value):

            raise ValueError(
                "Password must contain at least one uppercase letter"
            )

        if not re.search(r"[a-z]", value):

            raise ValueError(
                "Password must contain at least one lowercase letter"
            )

        if not re.search(r"[0-9]", value):

            raise ValueError(
                "Password must contain at least one number"
            )

        if not re.search(
            r"[!@#$%^&*(),.?\":{}|<>]",
            value
        ):

            raise ValueError(
                "Password must contain at least one special character"
            )

        return value


    # -----------------------------
    # CONFIRM PASSWORD VALIDATION
    # -----------------------------

    @model_validator(mode="after")
    def validate_confirm_password(self):

        if self.password != self.confirm_password:

            raise ValueError(
                "Passwords do not match"
            )

        return self


# -----------------------------
# USER RESPONSE
# -----------------------------

class UserResponse(BaseModel):

    user_id: UUID

    username: str

    full_name: str

    email: EmailStr

    role: str

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