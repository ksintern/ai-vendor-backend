from uuid import UUID

from sqlalchemy import (
    or_,
    asc,
    desc,
    func
)

from sqlalchemy.orm import Session

from app.models.vendor import Vendor
from app.models.category import Category
from app.models.subcategory import Subcategory
from app.models.review import Review
from app.models.pricing_model import PricingModel


# =====================================================
# CREATE VENDOR
# =====================================================

def create_vendor(

    db: Session,

    vendor_data: dict

):

    new_vendor = Vendor(

        **vendor_data

    )

    db.add(

        new_vendor

    )

    db.commit()

    db.refresh(

        new_vendor

    )

    return new_vendor


# =====================================================
# FETCH SINGLE
# =====================================================

def get_vendor_by_id(

    db: Session,

    vendor_id: UUID

):

    return (

        db.query(Vendor)

        .filter(

            Vendor.vendor_id == vendor_id,

            Vendor.is_active.is_(True)

        )

        .first()

    )


# =====================================================
# FETCH EMAIL
# =====================================================

def get_vendor_by_business_email(

    db: Session,

    business_email: str

):

    return (

        db.query(Vendor)

        .filter(

            Vendor.business_email

            == business_email

        )

        .first()

    )


# =====================================================
# FETCH SLUG
# =====================================================

def get_vendor_by_slug(

    db: Session,

    slug: str

):

    return (

        db.query(Vendor)

        .filter(

            Vendor.slug == slug

        )

        .first()

    )


# =====================================================
# FETCH ACTIVE
# =====================================================

def get_all_vendors(

    db: Session

):

    return (

        db.query(Vendor)

        .filter(

            Vendor.is_active.is_(True)

        )

        .all()

    )


# =====================================================
# SEARCH FILTER SORT
# =====================================================

def search_vendors(

    db: Session,

    query=None,

    city=None,

    category=None,

    subcategory=None,

    min_price=None,

    max_price=None,

    pricing_type=None,

    rating=None,

    min_reviews=None,

    available=None,

    verified=None,

    sort_by=None,

    page=1,

    limit=10

):

    search_query = (

        db.query(Vendor)

        .outerjoin(

            Review,

            Vendor.vendor_id

            ==

            Review.vendor_id

        )

        .outerjoin(

            PricingModel,

            Vendor.vendor_id

            ==

            PricingModel.vendor_id

        )

        .filter(

            Vendor.is_active.is_(True)

        )

    )


    # CATEGORY JOIN

    if category:

        search_query = search_query.join(

            Category,

            Vendor.category_id

            ==

            Category.category_id

        )


    # SUBCATEGORY JOIN

    if subcategory:

        search_query = search_query.join(

            Subcategory,

            Vendor.subcategory_id

            ==

            Subcategory.subcategory_id

        )


    # SEARCH

    if query:

        pattern = f"%{query}%"

        search_query = search_query.filter(

            or_(

                Vendor.name.ilike(

                    pattern

                ),

                Vendor.description.ilike(

                    pattern

                ),

                Vendor.city.ilike(

                    pattern

                )

            )

        )


    # CITY

    if city:

        search_query = search_query.filter(

            Vendor.city.ilike(

                f"%{city}%"

            )

        )


    # CATEGORY

    if category:

        search_query = search_query.filter(

            Category.name.ilike(

                f"%{category}%"

            )

        )


    # SUBCATEGORY

    if subcategory:

        search_query = search_query.filter(

            Subcategory.name.ilike(

                f"%{subcategory}%"

            )

        )


    # PRICE

    if min_price is not None:

        search_query = search_query.filter(

            Vendor.price_max >= min_price

        )


    if max_price is not None:

        search_query = search_query.filter(

            Vendor.price_min <= max_price

        )


    # PRICING TYPE

    if pricing_type:

        search_query = search_query.filter(

            PricingModel.pricing_type

            ==

            pricing_type

        )


    # VERIFIED

    if verified is not None:

        search_query = search_query.filter(

            Vendor.is_verified

            ==

            verified

        )


    # AVAILABLE

    if available is not None:

        search_query = search_query.filter(

            Vendor.is_available

            ==

            available

        )


    search_query = search_query.group_by(

        Vendor.vendor_id

    )


    # REAL REVIEW FILTER

    if rating:

        search_query = search_query.having(

            func.avg(

                Review.rating

            ) >= rating

        )


    # REVIEW COUNT

    if min_reviews:

        search_query = search_query.having(

            func.count(

                Review.review_id

            ) >= min_reviews

        )


    # SORT

    if sort_by:

        if sort_by == "rating":

            search_query = search_query.order_by(

                desc(

                    func.avg(

                        Review.rating

                    )

                )

            )


        elif sort_by == "price_low":

            search_query = search_query.order_by(

                asc(

                    Vendor.price_min

                )

            )


        elif sort_by == "price_high":

            search_query = search_query.order_by(

                desc(

                    Vendor.price_max

                )

            )


        elif sort_by == "latest":

            search_query = search_query.order_by(

                desc(

                    Vendor.created_at

                )

            )


    total = search_query.count()

    offset = (

        page - 1

    ) * limit


    vendors = (

        search_query

        .offset(

            offset

        )

        .limit(

            limit

        )

        .all()

    )


    return vendors,total


# =====================================================
# UPDATE
# =====================================================

def update_vendor(

    db: Session,

    vendor: Vendor,

    update_data: dict

):

    for key,value in update_data.items():

        setattr(

            vendor,

            key,

            value

        )

    db.commit()

    db.refresh(

        vendor

    )

    return vendor


# =====================================================
# SOFT DELETE
# =====================================================

def deactivate_vendor(

    db: Session,

    vendor: Vendor

):

    setattr(
        vendor,
        "is_active",
        False
    )

    db.commit()

    db.refresh(

        vendor

    )

    return vendor