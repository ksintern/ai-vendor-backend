from uuid import UUID

from fastapi import (
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from app.repositories.subcategory_repository import (

    create_subcategory,
    get_subcategory_by_id,
    get_subcategory_by_name,
    get_subcategory_by_slug,
    get_all_subcategories,
    update_subcategory,
    deactivate_subcategory
)

from app.repositories.category_repository import (
    get_category_by_id
)

from app.schemas.subcategory_schema import (
    SubcategoryCreateRequest
)


# -----------------------------
# CREATE SUBCATEGORY
# -----------------------------

def create_subcategory_service(
    db: Session,
    subcategory_data: SubcategoryCreateRequest
):

    # CHECK CATEGORY EXISTS

    category = get_category_by_id(

        db=db,

        category_id=subcategory_data.category_id
    )

    if category is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Parent category not found"
        )

    # CHECK DUPLICATE NAME

    existing_name = get_subcategory_by_name(

        db=db,

        name=subcategory_data.name
    )

    if existing_name is not None:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Subcategory name already exists"
        )

    # CHECK DUPLICATE SLUG

    existing_slug = get_subcategory_by_slug(

        db=db,

        slug=subcategory_data.slug
    )

    if existing_slug is not None:

        raise HTTPException(

            status_code=status.HTTP_400_BAD_REQUEST,

            detail="Subcategory slug already exists"
        )

    new_subcategory = create_subcategory(

        db=db,

        subcategory_data=subcategory_data.model_dump()
    )

    return {

        "success": True,

        "message": "Subcategory created successfully",

        "subcategory": new_subcategory
    }


# -----------------------------
# GET SINGLE SUBCATEGORY
# -----------------------------

def get_single_subcategory_service(
    db: Session,
    subcategory_id: UUID
):

    subcategory = get_subcategory_by_id(

        db=db,

        subcategory_id=subcategory_id
    )

    if subcategory is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Subcategory not found"
        )

    return {

        "success": True,

        "message": "Subcategory fetched successfully",

        "subcategory": subcategory
    }


# -----------------------------
# GET ALL SUBCATEGORIES
# -----------------------------

def get_all_subcategories_service(
    db: Session
):

    subcategories = get_all_subcategories(
        db=db
    )

    return {

        "success": True,

        "message": "Subcategories fetched successfully",

        "subcategories": subcategories
    }


# -----------------------------
# UPDATE SUBCATEGORY
# -----------------------------

def update_subcategory_service(
    db: Session,
    subcategory_id: UUID,
    update_data: dict
):

    subcategory = get_subcategory_by_id(

        db=db,

        subcategory_id=subcategory_id
    )

    if subcategory is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Subcategory not found"
        )

    # CHECK CATEGORY EXISTS

    if "category_id" in update_data:

        category = get_category_by_id(

            db=db,

            category_id=update_data["category_id"]
        )

        if category is None:

            raise HTTPException(

                status_code=status.HTTP_404_NOT_FOUND,

                detail="Parent category not found"
            )

    # CHECK DUPLICATE NAME

    if "name" in update_data:

        existing_name = get_subcategory_by_name(

            db=db,

            name=update_data["name"]
        )

        if (

            existing_name is not None
            and str(existing_name.subcategory_id)
            != str(subcategory.subcategory_id)

        ):

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Subcategory name already exists"
            )

    # CHECK DUPLICATE SLUG

    if "slug" in update_data:

        existing_slug = get_subcategory_by_slug(

            db=db,

            slug=update_data["slug"]
        )

        if (

            existing_slug is not None
            and str(existing_slug.subcategory_id)
            != str(subcategory.subcategory_id)

        ):

            raise HTTPException(

                status_code=status.HTTP_400_BAD_REQUEST,

                detail="Subcategory slug already exists"
            )

    updated_subcategory = update_subcategory(

        db=db,

        subcategory=subcategory,

        update_data=update_data
    )

    return {

        "success": True,

        "message": "Subcategory updated successfully",

        "subcategory": updated_subcategory
    }


# -----------------------------
# DEACTIVATE SUBCATEGORY
# -----------------------------

def deactivate_subcategory_service(
    db: Session,
    subcategory_id: UUID
):

    subcategory = get_subcategory_by_id(

        db=db,

        subcategory_id=subcategory_id
    )

    if subcategory is None:

        raise HTTPException(

            status_code=status.HTTP_404_NOT_FOUND,

            detail="Subcategory not found"
        )

    deactivated_subcategory = deactivate_subcategory(

        db=db,

        subcategory=subcategory
    )

    return {

        "success": True,

        "message": "Subcategory deactivated successfully",

        "subcategory": deactivated_subcategory
    }