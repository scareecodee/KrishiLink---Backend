from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(farmer.router)
app.include_router(buyer.router)
app.include_router(fpo.router)
app.include_router(admin.router)
app.include_router(common.router)


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
