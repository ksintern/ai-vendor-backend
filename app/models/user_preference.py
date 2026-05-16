import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class UserPreference(Base):
    __tablename__ = "user_preferences"

    preference_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False, unique=True
    )

    preferred_category_id = Column(
        UUID(as_uuid=True), ForeignKey("categories.category_id"), nullable=True
    )

    preferred_subcategory_id = Column(
        UUID(as_uuid=True), ForeignKey("subcategories.subcategory_id"), nullable=True
    )

    preferred_city = Column(String, nullable=True)

    preferred_price_range = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user = relationship("User", back_populates="preferences")

    preferred_category = relationship("Category")

    preferred_subcategory = relationship("Subcategory")
