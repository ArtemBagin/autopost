from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import User
from schemas import UserCreate, UserRead
from security import get_current_user, get_password_hash

router = APIRouter(
    tags=["Users"],
)


@router.post('/reg', status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.email == data.email))
    user = user.first()
    if user:
        raise HTTPException(status_code=422, detail="Email is already registered with us.")

    data = data.model_dump()
    hashed_password = get_password_hash(data.pop('password'))
    new_user = User(hashed_password=hashed_password, **data)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    payload = {"message": "User account has been succesfully created."}

    return JSONResponse(content=payload)


@router.post('/users/me', status_code=status.HTTP_200_OK, response_model=UserRead)
def get_user_detail(user: User = Depends(get_current_user)):
    return user
