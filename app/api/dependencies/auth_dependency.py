from jose import JWTError, jwt

from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app.core.config import settings

from app.db.session import get_db

from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/token"
)


# -----------------------------
# GET CURRENT AUTHENTICATED USER
# -----------------------------

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        email = payload.get("sub")

        if email is None:

            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:

        raise credentials_exception

    return user


# -----------------------------
# ROLE-BASED ACCESS CONTROL
# -----------------------------

def require_role(
    allowed_roles: list[str]
):

    def role_checker(

        current_user: User = Depends(
            get_current_user
        )
    ):

        if current_user.role not in allowed_roles:

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        return current_user

    return role_checker