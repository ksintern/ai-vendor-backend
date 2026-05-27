from uuid import UUID

from sqlalchemy import (
    or_,
    asc,
    desc,
    func
)

from sqlalchemy.orm import (
    Session,
    aliased
)

from app.models.vendor import Vendor
from app.models.review import Review
from app.models.service import Service


# =====================================
# CREATE ROOT VENDOR
# =====================================

def create_root_vendor(

    db: Session,

    current_user_id: UUID,

    vendor_data: dict

):

    existing=(

        db.query(Vendor)

        .filter(

            Vendor.user_id
            ==
            current_user_id

        )

        .first()

    )

    if existing:

        return existing

    vendor=Vendor(

        user_id=current_user_id,

        parent_vendor_id=None,

        **vendor_data

    )

    db.add(vendor)

    db.commit()

    db.refresh(vendor)

    return vendor


# =====================================
# CREATE CATEGORY VENDOR
# =====================================

def create_vendor(

    db: Session,

    vendor_data: dict

):

    vendor=Vendor(

        **vendor_data

    )

    db.add(vendor)

    db.commit()

    db.refresh(vendor)

    return vendor


# =====================================
# SERVICE
# =====================================

def create_service(

    db: Session,

    service: Service

):

    db.add(service)

    db.commit()

    db.refresh(service)

    return service


def get_service_by_id(

    db: Session,

    service_id: UUID

):

    return (

        db.query(Service)

        .filter(

            Service.service_id
            ==
            service_id

        )

        .first()

    )


def get_services_by_category(

    db: Session,

    category_vendor_id: UUID

):

    return (

        db.query(Service)

        .filter(

            Service.category_vendor_id
            ==
            category_vendor_id

        )

        .all()

    )


def service_exists(

    db: Session,

    category_vendor_id: UUID,

    service_name: str

):

    return (

        db.query(Service)

        .filter(

            Service.category_vendor_id
            ==
            category_vendor_id,

            func.lower(

                Service.service_name

            )

            ==

            service_name.strip().lower()

        )

        .first()

    )


def rename_service(

    db: Session,

    service: Service,

    service_name: str

):

    service.service_name=service_name

    db.commit()

    db.refresh(service)

    return service


def delete_service(

    db: Session,

    service: Service

):

    db.delete(service)

    db.commit()


# =====================================
# VENDOR
# =====================================

def get_vendor_by_id(

    db: Session,

    vendor_id: UUID

):

    return (

        db.query(Vendor)

        .filter(

            Vendor.vendor_id
            ==
            vendor_id,

            Vendor.is_active.is_(

                True

            )

        )

        .first()

    )


def get_vendor_by_business_email(

    db: Session,

    email: str

):

    return (

        db.query(Vendor)

        .filter(

            func.lower(

                Vendor.business_email

            )

            ==

            email.strip().lower()

        )

        .first()

    )


def get_all_vendors(

    db: Session

):

    return (

        db.query(Vendor)

        .filter(

            Vendor.parent_vendor_id.is_(

                None

            ),

            Vendor.is_active.is_(

                True

            )

        )

        .all()

    )


# =====================================
# SEARCH
# =====================================

def search_vendors(

    db: Session,

    query=None,

    city=None,

    category=None,

    min_price=None,

    max_price=None,

    rating=None,

    min_reviews=None,

    available=None,

    verified=None,

    sort_by=None,

    page=1,

    limit=10

):

    CategoryVendor=aliased(

        Vendor

    )

    search_query=(

        db.query(Vendor)

        .outerjoin(

            CategoryVendor,

            CategoryVendor.parent_vendor_id
            ==
            Vendor.vendor_id

        )

        .outerjoin(

            Service,

            Service.category_vendor_id
            ==
            CategoryVendor.vendor_id

        )

        .outerjoin(

            Review,

            Review.vendor_id
            ==
            Vendor.vendor_id

        )

        .filter(

            Vendor.parent_vendor_id.is_(

                None

            ),

            Vendor.is_active.is_(

                True

            )

        )

    )

    if query:

        pattern=f"%{query.strip()}%"

        search_query=(

            search_query

            .filter(

                or_(

                    Vendor.name.ilike(

                        pattern

                    ),

                    Vendor.description.ilike(

                        pattern

                    ),

                    Vendor.city.ilike(

                        pattern

                    ),

                    CategoryVendor.name.ilike(

                        pattern

                    ),

                    Service.service_name.ilike(

                        pattern

                    )

                )

            )

        )

    if city:

        search_query=(

            search_query

            .filter(

                Vendor.city.ilike(

                    f"%{city}%"

                )

            )

        )

    if category:

        search_query=(

            search_query

            .filter(

                CategoryVendor.name.ilike(

                    f"%{category}%"

                )

            )

        )

    # FIXED PRICE FILTERING

    if min_price is not None:

        search_query=(

            search_query

            .filter(

                Vendor.price_max

                >=

                min_price

            )

        )

    if max_price is not None:

        search_query=(

            search_query

            .filter(

                Vendor.price_min

                <=

                max_price

            )

        )

    if available is not None:

        search_query=(

            search_query

            .filter(

                Vendor.is_available

                ==

                available

            )

        )

    if verified is not None:

        search_query=(

            search_query

            .filter(

                Vendor.is_verified

                ==

                verified

            )

        )

    search_query=(

        search_query

        .group_by(

            Vendor.vendor_id

        )

    )

    if rating:

        search_query=(

            search_query

            .having(

                func.avg(

                    Review.rating

                )

                >=

                rating

            )

        )

    if min_reviews:

        search_query=(

            search_query

            .having(

                func.count(

                    Review.review_id

                )

                >=

                min_reviews

            )

        )

    if sort_by=="rating":

        search_query=(

            search_query

            .order_by(

                desc(

                    func.avg(

                        Review.rating

                    )

                )

            )

        )

    elif sort_by=="price_low":

        search_query=(

            search_query

            .order_by(

                asc(

                    Vendor.price_min

                )

            )

        )

    elif sort_by=="price_high":

        search_query=(

            search_query

            .order_by(

                desc(

                    Vendor.price_max

                )

            )

        )

    total=search_query.count()

    vendors=(

        search_query

        .offset(

            (page-1)*limit

        )

        .limit(

            limit

        )

        .all()

    )

    return vendors,total


# =====================================
# AI SEARCH
# =====================================

def search_vendors_ai(

    db: Session,

    filters: dict

):

    payload={

        "db":db,

        "page":1,

        "limit":10,

        "sort_by":"rating"

    }

    if filters.get(

        "city"

    ):

        payload["city"]=filters["city"]

    if filters.get(

        "category"

    ):

        payload["category"]=filters["category"]

    if filters.get(

        "budget"

    ):

        payload["max_price"]=filters["budget"]

    vendors,total=(

        search_vendors(

            **payload

        )

    )

    if not vendors:

        payload.pop(

            "category",

            None

        )

        vendors,total=(

            search_vendors(

                **payload

            )

        )

    return {

        "vendors":vendors,

        "total":total

    }

# =====================================
# UPDATE
# =====================================

def update_vendor(

    db: Session,

    vendor: Vendor,

    update_data: dict

):

    blocked = {

        "vendor_id",

        "user_id",

        "avg_rating",

        "review_count"

    }

    for key,value in update_data.items():

        if key in blocked:

            continue

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


# =====================================
# DELETE
# =====================================

def deactivate_vendor(

    db: Session,

    vendor: Vendor

):

    vendor.is_active=False

    db.commit()

    db.refresh(

        vendor

    )

    return vendor