from uuid import UUID

from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.subcategory_schema import (

    SubcategoryCreateRequest,

    SubcategoryUpdateRequest,

    SubcategoryDetailResponse,

    SubcategoryListResponse
)

from app.services.subcategory_service import (

    create_subcategory_service,

    get_single_subcategory_service,

    get_all_subcategories_service,

    update_subcategory_service,

    deactivate_subcategory_service
)

from app.api.dependencies.auth_dependency import (
    require_role
)

from app.models.user import User

from app.models.subcategory import Subcategory


router = APIRouter(

    prefix="/subcategories",

    tags=["Subcategories"]
)


# =====================================================
# CREATE SUBCATEGORY
# =====================================================

@router.post(
    "/",
    response_model=SubcategoryDetailResponse
)
def create_subcategory_api(

    subcategory_data: SubcategoryCreateRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_role(["admin"])
    )
):

    return create_subcategory_service(

        db=db,

        subcategory_data=subcategory_data
    )


# =====================================================
# GET SUBCATEGORIES BY CATEGORY
# =====================================================

@router.get(
    "/category/{category_id}"
)
def get_subcategories_by_category(

    category_id: UUID,

    db: Session = Depends(get_db)
):

    subcategories = db.query(Subcategory).filter(

        Subcategory.category_id == category_id,

        Subcategory.is_active == True

    ).all()

    return {

        "success": True,

        "message": "Subcategories fetched successfully",

        "subcategories": subcategories
    }


# =====================================================
# GET SINGLE SUBCATEGORY
# =====================================================

@router.get(
    "/{subcategory_id}",
    response_model=SubcategoryDetailResponse
)
def get_single_subcategory_api(

    subcategory_id: UUID,

    db: Session = Depends(get_db)
):

    return get_single_subcategory_service(

        db=db,

        subcategory_id=subcategory_id
    )


# =====================================================
# GET ALL SUBCATEGORIES
# =====================================================

@router.get(
    "/",
    response_model=SubcategoryListResponse
)
def get_all_subcategories_api(

    db: Session = Depends(get_db)
):

    return get_all_subcategories_service(

        db=db
    )


# =====================================================
# PARTIAL UPDATE SUBCATEGORY
# =====================================================

@router.patch(
    "/{subcategory_id}",
    response_model=SubcategoryDetailResponse
)
def update_subcategory_api(

    subcategory_id: UUID,

    subcategory_data: SubcategoryUpdateRequest,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_role(["admin"])
    )
):

    return update_subcategory_service(

        db=db,

        subcategory_id=subcategory_id,

        update_data=subcategory_data.model_dump(
            exclude_unset=True
        )
    )


# =====================================================
# DEACTIVATE SUBCATEGORY
# =====================================================

@router.delete(
    "/{subcategory_id}",
    response_model=SubcategoryDetailResponse
)
def deactivate_subcategory_api(

    subcategory_id: UUID,

    db: Session = Depends(get_db),

    current_user: User = Depends(
        require_role(["admin"])
    )
):

    return deactivate_subcategory_service(

        db=db,

        subcategory_id=subcategory_id
    )