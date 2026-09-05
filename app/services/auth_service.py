from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.user import User, FarmerProfile, BuyerProfile
from app.schemas.user import UserCreate
from app.utils.security import hash_password, verify_password, create_access_token, create_refresh_token
from datetime import timedelta
from app.config import get_settings

settings = get_settings()

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()

async def register_user(db: AsyncSession, user_create: UserCreate) -> User:
    existing = await get_user_by_email(db, user_create.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = hash_password(user_create.password)
    db_user = User(
        email=user_create.email,
        password_hash=hashed_pwd,
        full_name=user_create.full_name,
        user_type=user_create.user_type,
        phone=user_create.phone
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    
    if user_create.user_type.value == "farmer":
        db.add(FarmerProfile(user_id=db_user.id))
    elif user_create.user_type.value == "buyer":
        db.add(BuyerProfile(user_id=db_user.id))
    
    await db.commit()
    return db_user

async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

def create_tokens(user: User) -> dict:
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email, "role": user.user_type.value}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": user
    }
