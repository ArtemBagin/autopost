from fastapi import HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.user import UserRepository
from schemas.user import UserCreate
from security import get_password_hash


async def create_user(data: UserCreate, db: AsyncSession):
    user = await UserRepository(db).find_one(email=data.username)

    if user:
        raise HTTPException(
            status_code=422,
            detail="Email is already registered with us."
        )

    data = data.model_dump()
    data.update({'hashed_password': get_password_hash(data.pop('password'))})
    await UserRepository(db).add_one(data)
    payload = {"message": "User account has been succesfully created."}

    return JSONResponse(content=payload)