from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.vk import VkToken
from models.user import User
from security import get_current_user
from database.database import get_db
from services import vk_service

router = APIRouter(prefix='/api/token', tags=['token'])


@router.put('/vk', status_code=status.HTTP_200_OK)
async def add_vk_token(
        token: VkToken,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    res = await vk_service.add_vk_token(token, user, db)
    return res
