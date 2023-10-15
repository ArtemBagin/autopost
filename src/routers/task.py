from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.vk import TaskBase, VkTaskRead
from security import get_current_user
from database.database import get_db
from services import vk_service

router = APIRouter(prefix='/api/task', tags=['tasks'])


@router.post('/vk', status_code=status.HTTP_201_CREATED)
async def create_vk_task(
        task: TaskBase,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    new_task = await vk_service.create_vk_task(task, user, db)
    return VkTaskRead.model_validate(new_task)


@router.get('/vk/{pk}', response_model=VkTaskRead)
async def get_task(
        pk: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    task = await vk_service.check_and_get_task(db, user, pk)
    return task


@router.get('/vk', response_model=list[VkTaskRead])
async def get_tasks(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    tasks = await vk_service.get_tasks(user, db)
    return tasks

@router.delete('/vk/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def kill_vk_task(
        pk: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    res = await vk_service.kill_vk_task(pk, user, db)
    return res



