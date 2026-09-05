from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.database import init_db, AsyncSessionLocal

# Import all models so SQLAlchemy knows about them before create_all
import app.models.user       # noqa: F401
import app.models.crop       # noqa: F401
import app.models.market     # noqa: F401
import app.models.listing    # noqa: F401
import app.models.order      # noqa: F401
import app.models.notification  # noqa: F401

from app.utils.seed_data import seed_database
from app.routers import auth, farmer, buyer, fpo, admin, common

app = FastAPI(
    title="KrishiLink API",
    description="Smart Market Linkage & Price Discovery Platform for Farmers – SIH 2026",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration - Allow both local and production frontends
# Get allowed origins from environment variable or use default
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Add origins from environment variable (comma-separated)
if allowed_origins_env:
    env_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
    allowed_origins.extend(env_origins)

# Also check for VERCEL_URL or specific frontend URL
vercel_url = os.getenv("VERCEL_URL", "")
if vercel_url and vercel_url not in allowed_origins:
    allowed_origins.append(vercel_url)

# Remove duplicates while preserving order
allowed_origins = list(dict.fromkeys(allowed_origins))

print("Allowed CORS origins:", allowed_origins)  # Debug log

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

# Include routers - Note: You might want to add prefixes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(farmer.router, prefix="/api/farmer", tags=["Farmer"])
app.include_router(buyer.router, prefix="/api/buyer", tags=["Buyer"])
app.include_router(fpo.router, prefix="/api/fpo", tags=["FPO"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(common.router, prefix="/api/common", tags=["Common"])

@app.on_event("startup")
async def on_startup():
    await init_db()
    async with AsyncSessionLocal() as session:
        await seed_database(session)

@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Welcome to KrishiLink API",
        "docs": "/docs",
        "platform": "Smart Market Linkage & Price Discovery",
        "team": "EXCEPTION – SIH 2026",
    }

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy", "cors_origins": allowed_origins}