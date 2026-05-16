import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class SemanticEmbedding(Base):
    __tablename__ = "semantic_embeddings"

    embedding_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    vendor_id = Column(
        UUID(as_uuid=True), ForeignKey("vendors.vendor_id"), nullable=False, unique=True
    )

    embedding_reference = Column(String, nullable=False)

    model_name = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    vendor = relationship("Vendor", back_populates="semantic_embedding")
