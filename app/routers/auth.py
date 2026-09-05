from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.services import auth_service
from app.utils.security import get_current_user
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

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
