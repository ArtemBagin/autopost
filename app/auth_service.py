from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from config import settings
from models import User
from schemas import TokenResponse
from security import create_access_token, create_refresh_token, get_token_payload, verify_password


async def get_token(data: OAuth2PasswordRequestForm, db: AsyncSession):
    user = await db.execute(select(User).where(User.email == data.username))
    user = user.first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Email is not registered with us.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user[0]

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Login Credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return await _get_user_token(user=user)


async def get_refresh_token(token, db: AsyncSession):
    payload = get_token_payload(token=token)
    user_id: int | None = payload.get('id', None)
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await db.execute(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = user.first()
    user = user[0]
    return await _get_user_token(user=user, refresh_token=token)




async def _get_user_token(user: User, refresh_token=None):
    payload = {"id": user.id}

    access_token_expire = timedelta(minutes=settings.access_token_expire)

    access_token = await create_access_token(payload, access_token_expire)
    if not refresh_token:
        refresh_token_expire = timedelta(minutes=settings.refresh_token_expire)
        refresh_token = await create_refresh_token(payload, refresh_token_expire)
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=access_token_expire.seconds
    )