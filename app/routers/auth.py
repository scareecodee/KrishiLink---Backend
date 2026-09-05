from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services import auth_service
from app.utils.security import get_current_user
from app.models.user import User

# ============================================
# Router with /api/auth prefix (for production)
# ============================================
router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# ============================================
# Router WITHOUT /api prefix (for frontend compatibility)
# ============================================
no_prefix_router = APIRouter(prefix="/auth", tags=["Authentication (no prefix)"])

# ============================================
# OPTIONS handlers for no-prefix router
# ============================================

@no_prefix_router.options("/login")
async def options_login_no_prefix():
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

@no_prefix_router.options("/register")
async def options_register_no_prefix():
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

@no_prefix_router.options("/me")
async def options_me_no_prefix():
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

@no_prefix_router.options("/refresh-token")
async def options_refresh_token_no_prefix():
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

@no_prefix_router.options("/logout")
async def options_logout_no_prefix():
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
# Actual endpoints for no-prefix router
# ============================================

@no_prefix_router.post("/login", response_model=TokenResponse)
async def login_no_prefix(user_login: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login without /api prefix (for frontend compatibility)"""
    user = await auth_service.authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return auth_service.create_tokens(user)

@no_prefix_router.post("/register", response_model=TokenResponse)
async def register_no_prefix(user_create: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register without /api prefix (for frontend compatibility)"""
    user = await auth_service.register_user(db, user_create)
    return auth_service.create_tokens(user)

@no_prefix_router.get("/me", response_model=UserResponse)
async def get_me_no_prefix(current_user: User = Depends(get_current_user)):
    """Get current user without /api prefix (for frontend compatibility)"""
    return current_user

@no_prefix_router.post("/refresh-token")
async def refresh_token_no_prefix():
    """Refresh token without /api prefix (for frontend compatibility)"""
    return {"msg": "Token refreshed (stub)"}

@no_prefix_router.post("/logout")
async def logout_no_prefix():
    """Logout without /api prefix (for frontend compatibility)"""
    return {"msg": "Successfully logged out"}

# ============================================
# Original router with /api/auth prefix
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