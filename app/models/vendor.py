import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String, nullable=False)

    description = Column(Text, nullable=True)

    category_id = Column(
        UUID(as_uuid=True), ForeignKey("categories.category_id"), nullable=False
    )

    subcategory_id = Column(
        UUID(as_uuid=True), ForeignKey("subcategories.subcategory_id"), nullable=False
    )

    city = Column(String, nullable=False)

    address = Column(Text, nullable=True)

    contact_email = Column(String, nullable=False)

    contact_phone = Column(String, nullable=False)

    price_min = Column(Integer, nullable=True)

    price_max = Column(Integer, nullable=True)

    avg_rating = Column(Float, default=0.0)

    review_count = Column(Integer, default=0)

    is_available = Column(Boolean, default=True)

    is_verified = Column(Boolean, default=False)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    category = relationship("Category", back_populates="vendors")

    subcategory = relationship("Subcategory", back_populates="vendors")

    reviews = relationship("Review", back_populates="vendor")

    services = relationship("VendorService", back_populates="vendor")

    pricing_models = relationship("PricingModel", back_populates="vendor")

    media = relationship("VendorMedia", back_populates="vendor")

    viewed_by = relationship("ViewedVendor", back_populates="vendor")

    recommendation_metadata = relationship(
        "RecommendationMetadata", back_populates="vendor", uselist=False
    )

    semantic_embedding = relationship(
        "SemanticEmbedding", back_populates="vendor", uselist=False
    )
