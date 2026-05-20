from uuid import UUID

from pydantic import (
    BaseModel,
    Field
)


# -----------------------------
# SUBCATEGORY BASE
# -----------------------------

class SubcategoryBase(BaseModel):

    category_id: UUID

    name: str = Field(
        min_length=2,
        max_length=255
    )

    slug: str = Field(
        min_length=2,
        max_length=255
    )

    description: str | None = None


# -----------------------------
# CREATE SUBCATEGORY
# -----------------------------

class SubcategoryCreateRequest(
    SubcategoryBase
):

    pass


# -----------------------------
# UPDATE SUBCATEGORY
# -----------------------------

class SubcategoryUpdateRequest(
    BaseModel
):

    category_id: UUID | None = None

    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )

    slug: str | None = Field(
        default=None,
        min_length=2,
        max_length=255
    )

    description: str | None = None

    is_active: bool | None = None


# -----------------------------
# SUBCATEGORY RESPONSE
# -----------------------------

class SubcategoryResponse(
    SubcategoryBase
):

    subcategory_id: UUID

    is_active: bool

    class Config:

        from_attributes = True


# -----------------------------
# SINGLE SUBCATEGORY RESPONSE
# -----------------------------

class SubcategoryDetailResponse(
    BaseModel
):

    success: bool

    message: str

    subcategory: SubcategoryResponse


# -----------------------------
# SUBCATEGORY LIST RESPONSE
# -----------------------------

class SubcategoryListResponse(
    BaseModel
):

    success: bool

    message: str

    subcategories: list[
        SubcategoryResponse
    ]