from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.auth import router as auth_router

from app.api.routes.vendor import router as vendor_router

from app.api.routes.category import router as category_router

from app.api.routes.subcategory import router as subcategory_router

from app.db.base import Base

from app.db.session import engine


# -----------------------------
# IMPORT ALL MODELS
# -----------------------------

from app.models.user import User

from app.models.category import Category

from app.models.subcategory import Subcategory

from app.models.vendor import Vendor


# -----------------------------
# CREATE DATABASE TABLES
# -----------------------------

Base.metadata.create_all(bind=engine)


app = FastAPI(

    title="AI Vendor Discovery Agent API"
)


# -----------------------------
# CORS CONFIGURATION
# -----------------------------

origins = [

    "http://localhost:5173",
]


app.add_middleware(

    CORSMiddleware,

    allow_origins=origins,

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# -----------------------------
# ROOT ROUTE
# -----------------------------

@app.get("/")
def home():

    return {

        "message": "AI Vendor Discovery Agent Backend Running"
    }


# -----------------------------
# AUTH ROUTES
# -----------------------------

app.include_router(auth_router)


# -----------------------------
# CATEGORY ROUTES
# -----------------------------

app.include_router(category_router)


# -----------------------------
# SUBCATEGORY ROUTES
# -----------------------------

app.include_router(subcategory_router)


# -----------------------------
# VENDOR ROUTES
# -----------------------------

app.include_router(vendor_router)