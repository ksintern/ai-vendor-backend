import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String
)

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.sql import func

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    full_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    phone_number = Column(
        String,
        nullable=True
    )

    # NEW ROLE FIELD
    role = Column(
        String,
        nullable=False,
        default="user"
    )

    password_hash = Column(
        String,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # TEMPORARILY COMMENTED FOR AUTH MODULE TESTING

    # reviews = relationship(
    #     "Review",
    #     back_populates="user"
    # )

    # viewed_vendors = relationship(
    #     "ViewedVendor",
    #     back_populates="user"
    # )

    # preferences = relationship(
    #     "UserPreference",
    #     back_populates="user",
    #     uselist=False
    # )

    # conversations = relationship(
    #     "Conversation",
    #     back_populates="user"
    # )

    # search_history = relationship(
    #     "SearchHistory",
    #     back_populates="user"
    # )