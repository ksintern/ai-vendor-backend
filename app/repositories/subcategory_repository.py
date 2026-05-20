from uuid import UUID

from sqlalchemy.orm import Session

from app.models.subcategory import Subcategory


# -----------------------------
# CREATE SUBCATEGORY
# -----------------------------

def create_subcategory(
    db: Session,
    subcategory_data: dict
):

    new_subcategory = Subcategory(
        **subcategory_data
    )

    db.add(new_subcategory)

    db.commit()

    db.refresh(new_subcategory)

    return new_subcategory


# -----------------------------
# GET SUBCATEGORY BY ID
# -----------------------------

def get_subcategory_by_id(
    db: Session,
    subcategory_id: UUID
):

    return db.query(Subcategory).filter(

        Subcategory.subcategory_id == subcategory_id,

        Subcategory.is_active.is_(True)

    ).first()


# -----------------------------
# GET SUBCATEGORY BY NAME
# -----------------------------

def get_subcategory_by_name(
    db: Session,
    name: str
):

    return db.query(Subcategory).filter(

        Subcategory.name == name

    ).first()


# -----------------------------
# GET SUBCATEGORY BY SLUG
# -----------------------------

def get_subcategory_by_slug(
    db: Session,
    slug: str
):

    return db.query(Subcategory).filter(

        Subcategory.slug == slug

    ).first()


# -----------------------------
# GET ALL SUBCATEGORIES
# -----------------------------

def get_all_subcategories(
    db: Session
):

    return db.query(Subcategory).filter(

        Subcategory.is_active.is_(True)

    ).all()


# -----------------------------
# UPDATE SUBCATEGORY
# -----------------------------

def update_subcategory(
    db: Session,
    subcategory: Subcategory,
    update_data: dict
):

    for key, value in update_data.items():

        setattr(
            subcategory,
            key,
            value
        )

    db.commit()

    db.refresh(subcategory)

    return subcategory


# -----------------------------
# DEACTIVATE SUBCATEGORY
# -----------------------------

def deactivate_subcategory(
    db: Session,
    subcategory: Subcategory
):

    setattr(
        subcategory,
        "is_active",
        False
    )

    db.commit()

    db.refresh(subcategory)

    return subcategory