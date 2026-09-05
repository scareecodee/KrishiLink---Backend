from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
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

# CORS Configuration
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

if allowed_origins_env:
    env_origins = [origin.strip() for origin in allowed_origins_env.split(",") if origin.strip()]
    allowed_origins.extend(env_origins)

allowed_origins = list(dict.fromkeys(allowed_origins))
print("Allowed CORS origins:", allowed_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# ============================================
# IMPORTANT: Include routers with AND without prefix
# ============================================

# 1. Include with /api prefix (for production)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(farmer.router, prefix="/api/farmer", tags=["Farmer"])
app.include_router(buyer.router, prefix="/api/buyer", tags=["Buyer"])
app.include_router(fpo.router, prefix="/api/fpo", tags=["FPO"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(common.router, prefix="/api/common", tags=["Common"])

# 2. Include WITHOUT prefix (for compatibility with your frontend)
app.include_router(auth.router, tags=["Authentication (no prefix)"])
app.include_router(farmer.router, tags=["Farmer (no prefix)"])
app.include_router(buyer.router, tags=["Buyer (no prefix)"])
app.include_router(fpo.router, tags=["FPO (no prefix)"])
app.include_router(admin.router, tags=["Admin (no prefix)"])
app.include_router(common.router, tags=["Common (no prefix)"])

# ============================================
# Global OPTIONS handler for CORS preflight
# ============================================
@app.options("/{path:path}")
async def options_handler():
    """Handle OPTIONS preflight requests for all routes"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

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