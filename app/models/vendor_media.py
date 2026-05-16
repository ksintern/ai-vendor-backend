import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class VendorMedia(Base):
    __tablename__ = "vendor_media"

    media_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vendor_id = Column(
        UUID(as_uuid=True), ForeignKey("vendors.vendor_id"), nullable=False
    )

    media_url = Column(String, nullable=False)

    media_type = Column(String, nullable=False)

    title = Column(String, nullable=True)

    is_primary = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    vendor = relationship("Vendor", back_populates="media")
