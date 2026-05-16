import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Subcategory(Base):
    __tablename__ = "subcategories"

    subcategory_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categories.category_id"),
        nullable=False
    )

    name = Column(
        String,
        nullable=False,
        unique=True
    )

    slug = Column(
        String,
        unique=True,
        nullable=True
    )

    description = Column(
        Text,
        nullable=True
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

    category = relationship(
        "Category",
        back_populates="subcategories"
    )

    vendors = relationship(
        "Vendor",
        back_populates="subcategory"
    )