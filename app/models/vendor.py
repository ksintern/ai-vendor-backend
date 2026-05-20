from uuid import uuid4

from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey
)

from sqlalchemy.orm import relationship

from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

from app.models.vendor_service import VendorService
from app.models.review import Review
from app.models.pricing_model import PricingModel
from app.models.vendor_media import VendorMedia
from app.models.viewed_vendor import ViewedVendor


class Vendor(Base):

    __tablename__ = "vendors"


    # =====================================================
    # PRIMARY KEY
    # =====================================================

    vendor_id = Column(

        UUID(as_uuid=True),

        primary_key=True,

        default=uuid4
    )


    # =====================================================
    # USER RELATION
    # =====================================================

    user_id = Column(

        UUID(as_uuid=True),

        ForeignKey(
            "users.user_id"
        ),

        nullable=True,

        unique=True
    )


    # =====================================================
    # PARENT CHILD HIERARCHY
    # =====================================================

    parent_vendor_id = Column(

        UUID(as_uuid=True),

        ForeignKey(
            "vendors.vendor_id"
        ),

        nullable=True
    )


    # =====================================================
    # BASIC DETAILS
    # =====================================================

    name = Column(

        String,

        nullable=False
    )

    slug = Column(

        String,

        unique=True,

        nullable=True
    )

    description = Column(

        String,

        nullable=True
    )


    # =====================================================
    # CATEGORY
    # =====================================================

    category_id = Column(

        UUID(as_uuid=True),

        ForeignKey(
            "categories.category_id"
        ),

        nullable=True
    )

    subcategory_id = Column(

        UUID(as_uuid=True),

        ForeignKey(
            "subcategories.subcategory_id"
        ),

        nullable=True
    )


    # =====================================================
    # LOCATION
    # =====================================================

    city = Column(

        String,

        nullable=True
    )

    address = Column(

        String,

        nullable=True
    )


    # =====================================================
    # CONTACT
    # =====================================================

    business_email = Column(

        String,

        nullable=False
    )

    contact_phone = Column(

        String,

        nullable=False
    )


    # =====================================================
    # PRICING
    # =====================================================

    price_min = Column(

        Integer,

        nullable=True
    )

    price_max = Column(

        Integer,

        nullable=True
    )


    # =====================================================
    # REVIEW SUMMARY
    # =====================================================

    avg_rating = Column(

        Integer,

        default=0
    )

    review_count = Column(

        Integer,

        default=0
    )


    # =====================================================
    # STATUS
    # =====================================================

    is_available = Column(

        Boolean,

        default=True
    )

    is_verified = Column(

        Boolean,

        default=False
    )

    is_active = Column(

        Boolean,

        default=True
    )


    # =====================================================
    # RELATIONSHIPS
    # =====================================================

    user = relationship(

        "User",

        back_populates="vendor"
    )


    category = relationship(

        "Category"
    )


    subcategory = relationship(

        "Subcategory"
    )


    reviews = relationship(

        "Review",

        back_populates="vendor",

        cascade="all, delete-orphan"
    )


    pricing_models = relationship(

        "PricingModel",

        back_populates="vendor",

        cascade="all, delete-orphan"
    )


    services = relationship(

        "VendorService",

        back_populates="vendor",

        cascade="all, delete-orphan"
    )


    media = relationship(

        "VendorMedia",

        back_populates="vendor",

        cascade="all, delete-orphan"
    )


    viewed_by = relationship(

        "ViewedVendor",

        back_populates="vendor",

        cascade="all, delete-orphan"
    )


    # =====================================================
    # PARENT VENDOR
    # =====================================================

    parent_vendor = relationship(

        "Vendor",

        remote_side=[

            vendor_id

        ],

        back_populates=

        "managed_teams"
    )


    # =====================================================
    # MANAGED INTERNAL TEAMS
    # =====================================================

    managed_teams = relationship(

        "Vendor",

        back_populates=

        "parent_vendor",

        cascade=

        "all, delete-orphan"
    )