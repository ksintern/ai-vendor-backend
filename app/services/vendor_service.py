from uuid import UUID

from fastapi import (
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.vendor import Vendor

from app.repositories.vendor_repository import (

    get_vendor_by_business_email,

    get_vendor_by_id,

    get_vendor_by_slug,

    get_all_vendors,

    search_vendors,

    update_vendor,

    deactivate_vendor
)

from app.schemas.vendor_schema import (

    VendorProfileUpdateRequest
)


# =====================================================
# CREATE INTERNAL TEAM
# =====================================================

def create_internal_team_service(

    db: Session,

    current_user: User,

    team_name: str,

    category_id: UUID,

    description: str | None = None

):

    parent_vendor = (

        db.query(Vendor)

        .filter(

            Vendor.user_id

            ==

            current_user.user_id

        )

        .first()

    )

    if parent_vendor is None:

        raise HTTPException(

            status_code=404,

            detail="Parent vendor not found"

        )

    child_vendor = Vendor(

        parent_vendor_id=

        parent_vendor.vendor_id,

        name=team_name,

        description=description,

        category_id=category_id,

        business_email=

        parent_vendor.business_email,

        contact_phone=

        parent_vendor.contact_phone,

        city=

        parent_vendor.city,

        address=

        parent_vendor.address,

        is_available=True,

        is_active=True

    )

    db.add(

        child_vendor

    )

    db.commit()

    db.refresh(

        child_vendor

    )

    return child_vendor


# =====================================================
# FETCH INTERNAL TEAMS
# =====================================================

def get_internal_teams_service(

    db: Session,

    current_user: User

):

    parent_vendor = (

        db.query(Vendor)

        .filter(

            Vendor.user_id

            ==

            current_user.user_id

        )

        .first()

    )

    if parent_vendor is None:

        raise HTTPException(

            status_code=404,

            detail="Vendor not found"

        )

    teams = (

        db.query(Vendor)

        .filter(

            Vendor.parent_vendor_id

            ==

            parent_vendor.vendor_id

        )

        .all()

    )

    return teams


# =====================================================
# CURRENT PROFILE
# =====================================================

def get_current_vendor_profile_service(

    db: Session,

    current_user: User

):

    vendor = (

        db.query(Vendor)

        .filter(

            Vendor.user_id

            ==

            current_user.user_id

        )

        .first()

    )

    if vendor is None:

        raise HTTPException(

            status_code=

            status.HTTP_404_NOT_FOUND,

            detail=

            "Vendor profile not found"

        )

    return {

        "success": True,

        "message":

        "Vendor profile fetched successfully",

        "vendor": vendor

    }


# =====================================================
# UPDATE PROFILE
# =====================================================

def update_current_vendor_profile_service(

    db: Session,

    current_user: User,

    vendor_data:

    VendorProfileUpdateRequest

):

    vendor = (

        db.query(Vendor)

        .filter(

            Vendor.user_id

            ==

            current_user.user_id

        )

        .first()

    )

    if vendor is None:

        raise HTTPException(

            status_code=404,

            detail=

            "Vendor profile not found"

        )

    update_data = (

        vendor_data.model_dump(

            exclude_unset=True

        )

    )


    # DUPLICATE SLUG

    if "slug" in update_data:

        existing_slug = (

            get_vendor_by_slug(

                db=db,

                slug=

                update_data["slug"]

            )

        )

        if (

            existing_slug

            and

            existing_slug.vendor_id

            !=

            vendor.vendor_id

        ):

            raise HTTPException(

                status_code=400,

                detail=

                "Vendor slug already exists"

            )


    # DUPLICATE EMAIL

    if "business_email" in update_data:

        existing_email = (

            get_vendor_by_business_email(

                db=db,

                business_email=

                update_data[

                    "business_email"

                ]

            )

        )

        if (

            existing_email

            and

            existing_email.vendor_id

            !=

            vendor.vendor_id

        ):

            raise HTTPException(

                status_code=400,

                detail=

                "Business email already exists"

            )


    updated_vendor = (

        update_vendor(

            db=db,

            vendor=vendor,

            update_data=

            update_data

        )

    )

    return {

        "success": True,

        "message":

        "Vendor profile updated successfully",

        "vendor":

        updated_vendor

    }


# =====================================================
# FETCH SINGLE
# =====================================================

def get_single_vendor_service(

    db: Session,

    vendor_id: UUID

):

    vendor = (

        get_vendor_by_id(

            db=db,

            vendor_id=

            vendor_id

        )

    )

    if vendor is None:

        raise HTTPException(

            status_code=404,

            detail=

            "Vendor not found"

        )

    return {

        "success": True,

        "message":

        "Vendor fetched successfully",

        "vendor": vendor

    }


# =====================================================
# FETCH ALL
# =====================================================

def get_all_vendors_service(

    db: Session

):

    vendors = (

        get_all_vendors(

            db=db

        )

    )

    return {

        "success": True,

        "message":

        "Vendor list fetched successfully",

        "page": 1,

        "limit":

        len(vendors),

        "total_results":

        len(vendors),

        "vendors":

        vendors

    }


# =====================================================
# SEARCH
# =====================================================

def search_vendors_service(

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

    if page < 1:

        raise HTTPException(

            status_code=400,

            detail=

            "Page must be > 0"

        )

    if (

        limit < 1

        or

        limit > 100

    ):

        raise HTTPException(

            status_code=400,

            detail=

            "Limit must be 1-100"

        )

    vendors,total = (

        search_vendors(

            db=db,

            query=query,

            city=city,

            category=category,

            subcategory=subcategory,

            min_price=min_price,

            max_price=max_price,

            pricing_type=pricing_type,

            rating=rating,

            min_reviews=min_reviews,

            available=available,

            verified=verified,

            sort_by=sort_by,

            page=page,

            limit=limit

        )

    )

    return {

        "success": True,

        "message":

        "Vendor filters applied successfully",

        "page": page,

        "limit": limit,

        "total_results":

        total,

        "vendors":

        vendors

    }


# =====================================================
# DEACTIVATE
# =====================================================

def deactivate_vendor_service(

    db: Session,

    vendor_id: UUID

):

    vendor = (

        get_vendor_by_id(

            db=db,

            vendor_id=

            vendor_id

        )

    )

    if vendor is None:

        raise HTTPException(

            status_code=404,

            detail=

            "Vendor not found"

        )

    vendor = (

        deactivate_vendor(

            db=db,

            vendor=vendor

        )

    )

    return {

        "success": True,

        "message":

        "Vendor deactivated successfully",

        "vendor": vendor

    }