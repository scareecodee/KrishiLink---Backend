from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services import auth_service
from app.utils.security import get_current_user
from app.models.user import User

# Create router with /api/auth prefix
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# ============================================
# OPTIONS handlers for CORS preflight
# These handle both /auth/* and /api/auth/* paths
# ============================================

@router.options("/login")
async def options_login():
    """Handle OPTIONS preflight for /api/auth/login"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

@router.options("/register")
async def options_register():
    """Handle OPTIONS preflight for /api/auth/register"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

@router.options("/me")
async def options_me():
    """Handle OPTIONS preflight for /api/auth/me"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

@router.options("/refresh-token")
async def options_refresh_token():
    """Handle OPTIONS preflight for /api/auth/refresh-token"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

@router.options("/logout")
async def options_logout():
    """Handle OPTIONS preflight for /api/auth/logout"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

# Also handle OPTIONS for paths without /api prefix
# These are for frontend compatibility
@router.options("/api/auth/login")
async def options_api_login():
    """Handle OPTIONS preflight for /api/auth/login (explicit)"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

@router.options("/api/auth/register")
async def options_api_register():
    """Handle OPTIONS preflight for /api/auth/register (explicit)"""
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type, Accept, X-Requested-With",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "600",
        }
    )

# ============================================
# Your actual endpoints
# ============================================

@router.post("/register", response_model=TokenResponse)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register_user(db, user_create)
    return auth_service.create_tokens(user)

@router.post("/login", response_model=TokenResponse)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await auth_service.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return auth_service.create_tokens(user)

@router.post("/refresh-token")
async def refresh_token():
    return {"msg": "Token refreshed (stub)"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
async def logout():
    return {"msg": "Successfully logged out"}