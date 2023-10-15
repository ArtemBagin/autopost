from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_db
from services import user_service
from models.user import User
from schemas.user import UserCreate, UserRead
from security import get_current_user

router = APIRouter(
    tags=["Users"],
)


@router.post('/reg', status_code=status.HTTP_201_CREATED)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    res = await user_service.create_user(data, db)
    return res


@router.post('/users/me', status_code=status.HTTP_200_OK, response_model=UserRead)
def get_user_detail(user: User = Depends(get_current_user)):
    return user
