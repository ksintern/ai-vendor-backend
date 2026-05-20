from uuid import UUID

from fastapi import (

    APIRouter,

    Depends,

    Query
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.vendor_schema import (

    VendorProfileUpdateRequest,

    VendorDetailResponse,

    VendorListResponse
)

from app.services.vendor_service import (

    get_current_vendor_profile_service,

    update_current_vendor_profile_service,

    get_single_vendor_service,

    get_all_vendors_service,

    search_vendors_service,

    deactivate_vendor_service
)

from app.api.dependencies.auth_dependency import (

    require_role
)

from app.models.user import User


router = APIRouter(

    prefix="/vendors",

    tags=["Vendors"]
)


# =====================================================
# CURRENT PROFILE
# =====================================================

@router.get(

    "/profile",

    response_model=VendorDetailResponse
)
def get_current_vendor_profile_api(

    db: Session = Depends(get_db),

    current_user: User = Depends(

        require_role(["vendor"])
    )
):

    return get_current_vendor_profile_service(

        db=db,

        current_user=current_user
    )


# =====================================================
# UPDATE PROFILE
# =====================================================

@router.put(

    "/profile",

    response_model=VendorDetailResponse
)
def update_current_vendor_profile_api(

    vendor_data: VendorProfileUpdateRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(

        require_role(["vendor"])
    )
):

    return update_current_vendor_profile_service(

        db=db,

        current_user=current_user,

        vendor_data=vendor_data
    )


# =====================================================
# SEARCH + FILTER API
# =====================================================

@router.get(

    "/search",

    response_model=VendorListResponse
)
def search_vendors_api(

    query: str | None = Query(None),

    city: str | None = Query(None),

    category: str | None = Query(None),

    subcategory: str | None = Query(None),

    min_price: int | None = Query(None),

    max_price: int | None = Query(None),

    pricing_type: str | None = Query(None),

    rating: float | None = Query(None),

    min_reviews: int | None = Query(None),

    available: bool | None = Query(None),

    verified: bool | None = Query(None),

    sort_by: str | None = Query(

        None,

        description=

        "rating | price_low | price_high | latest"
    ),

    page: int = Query(

        1,

        ge=1
    ),

    limit: int = Query(

        10,

        ge=1,

        le=100
    ),

    db: Session = Depends(get_db)
):

    return search_vendors_service(

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


# =====================================================
# SINGLE VENDOR
# =====================================================

@router.get(

    "/{vendor_id}",

    response_model=VendorDetailResponse
)
def get_single_vendor_api(

    vendor_id: UUID,

    db: Session = Depends(get_db)
):

    return get_single_vendor_service(

        db=db,

        vendor_id=vendor_id
    )


# =====================================================
# ALL VENDORS
# =====================================================

@router.get(

    "/",

    response_model=VendorListResponse
)
def get_all_vendors_api(

    db: Session = Depends(get_db)
):

    return get_all_vendors_service(

        db=db
    )


# =====================================================
# SOFT DELETE
# =====================================================

@router.delete(

    "/{vendor_id}",

    response_model=VendorDetailResponse
)
def deactivate_vendor_api(

    vendor_id: UUID,

    db: Session = Depends(get_db),

    current_user: User = Depends(

        require_role(["admin"])
    )
):

    return deactivate_vendor_service(

        db=db,

        vendor_id=vendor_id
    )