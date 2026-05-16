import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class PricingModel(Base):
    __tablename__ = "pricing_models"

    pricing_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vendor_id = Column(
        UUID(as_uuid=True), ForeignKey("vendors.vendor_id"), nullable=False
    )

    title = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    price = Column(Integer, nullable=False)

    pricing_type = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    vendor = relationship("Vendor", back_populates="pricing_models")
