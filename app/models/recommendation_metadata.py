import uuid

from sqlalchemy import Column, DateTime, Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class RecommendationMetadata(Base):
    __tablename__ = "recommendation_metadata"

    metadata_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vendor_id = Column(
        UUID(as_uuid=True), ForeignKey("vendors.vendor_id"), nullable=False, unique=True
    )

    recommendation_score = Column(Float, default=0.0)

    popularity_score = Column(Float, default=0.0)

    engagement_score = Column(Float, default=0.0)

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    vendor = relationship("Vendor", back_populates="recommendation_metadata")
