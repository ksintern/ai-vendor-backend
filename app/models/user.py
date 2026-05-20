import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    String
)

from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

from app.models.review import Review

from app.models.search_history import SearchHistory

from app.models.viewed_vendor import ViewedVendor

from app.models.user_preference import UserPreference

from app.models.vendor import Vendor

from app.models.conversation import Conversation

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

    # NEW USERNAME FIELD
    username = Column(
        String,
        unique=True,
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

    # ROLE FIELD
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


    # -----------------------------
    # VENDOR RELATIONSHIP (NEW)
    # -----------------------------

    vendor = relationship(
        "Vendor",
        back_populates="user",
        uselist=False
    )


    # TEMPORARILY COMMENTED FOR AUTH MODULE TESTING

    reviews = relationship(
        "Review",
        back_populates="user"
    )

    viewed_vendors = relationship(
        "ViewedVendor",
        back_populates="user"
    )

    preferences = relationship(
        "UserPreference",
        back_populates="user",
        uselist=False
    )

    conversations = relationship(
        "Conversation",
        back_populates="user"
    )

    search_history = relationship(
        "SearchHistory",
        back_populates="user"
    )