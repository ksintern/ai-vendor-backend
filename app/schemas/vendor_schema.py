from uuid import UUID

from pydantic import (

    BaseModel,

    EmailStr,

    Field,

    field_validator,

    model_validator
)

import re


# =====================================================
# INTERNAL TEAM SCHEMA
# =====================================================

class ManagedTeamRequest(

    BaseModel
):

    team_name: str

    category_id: UUID

    subcategory_ids: list[UUID]


class ManagedTeamResponse(

    BaseModel
):

    vendor_id: UUID

    name: str

    category_id: UUID | None

    subcategory_ids: list[UUID]

    class Config:

        from_attributes = True


# =====================================================
# VENDOR PROFILE BASE
# =====================================================

class VendorProfileBase(

    BaseModel
):

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

    category_id: UUID | None = None

    subcategory_id: UUID | None = None

    city: str | None = Field(

        default=None,

        min_length=2,

        max_length=255
    )

    address: str | None = None

    business_email: EmailStr | None = None

    contact_phone: str | None = Field(

        default=None,

        min_length=10,

        max_length=15
    )

    price_min: int | None = None

    price_max: int | None = None

    is_available: bool | None = True


    @field_validator(

        "contact_phone"

    )
    @classmethod
    def validate_phone(

        cls,

        value
    ):

        if value is None:

            return value

        cleaned = value.replace(

            " ",

            ""
        )

        if not re.match(

            r"^[0-9+\-()]+$",

            cleaned
        ):

            raise ValueError(

                "Invalid phone number format"
            )

        return cleaned


    @field_validator(

        "slug"

    )
    @classmethod
    def validate_slug(

        cls,

        value
    ):

        if value is None:

            return value

        if not re.match(

            r"^[a-z0-9-]+$",

            value
        ):

            raise ValueError(

                "Slug must contain lowercase letters numbers hyphens"
            )

        return value


    @model_validator(

        mode="after"
    )
    def validate_price_range(

        self
    ):

        if (

            self.price_min is not None

            and

            self.price_max is not None

            and

            self.price_min > self.price_max

        ):

            raise ValueError(

                "Minimum price cannot exceed maximum price"
            )

        return self


# =====================================================
# PROFILE UPDATE
# =====================================================

class VendorProfileUpdateRequest(

    VendorProfileBase

):

    pass


# =====================================================
# SEARCH REQUEST
# =====================================================

class VendorSearchRequest(

    BaseModel
):

    query: str | None = None

    city: str | None = None

    category: str | None = None

    subcategory: str | None = None

    min_price: int | None = None

    max_price: int | None = None

    rating: float | None = None

    min_reviews: int | None = None

    available: bool | None = None

    verified: bool | None = None

    sort_by: str | None = None

    page: int = 1

    limit: int = 10


# =====================================================
# VENDOR RESPONSE
# =====================================================

class VendorResponse(

    BaseModel
):

    vendor_id: UUID

    user_id: UUID | None

    parent_vendor_id: UUID | None

    name: str | None

    slug: str | None

    description: str | None

    category_id: UUID | None

    subcategory_id: UUID | None

    city: str | None

    address: str | None

    business_email: EmailStr | None

    contact_phone: str | None

    price_min: int | None

    price_max: int | None

    avg_rating: float

    review_count: int

    is_available: bool

    is_verified: bool

    is_active: bool

    managed_teams: list[ManagedTeamResponse] = []


    class Config:

        from_attributes = True


# =====================================================
# SINGLE RESPONSE
# =====================================================

class VendorDetailResponse(

    BaseModel
):

    success: bool

    message: str

    vendor: VendorResponse


# =====================================================
# MULTIPLE RESPONSE
# =====================================================

class VendorListResponse(

    BaseModel
):

    success: bool

    message: str

    page: int

    limit: int

    total_results: int

    vendors: list[VendorResponse]