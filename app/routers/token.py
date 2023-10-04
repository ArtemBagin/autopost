from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import VkToken
from models import User
from security import get_current_user
from database import get_db

router = APIRouter(prefix='/api/token', tags=['token'])


@router.put('/vk', status_code=status.HTTP_200_OK)
async def add_vk_token(
        token: VkToken,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    user.vk_token = token.token
    await db.commit()
    return {'status': 'token successfully changed'}
