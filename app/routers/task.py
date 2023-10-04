from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, VkTask
from schemas import VkTaskCreate, TaskBase, VkTaskRead
from security import get_current_user
from database import get_db
from autopost.autopost import create_task, kill_task, VkSend

router = APIRouter(prefix='/api/task', tags=['tasks'])


@router.post('/vk', status_code=status.HTTP_201_CREATED)
async def create_vk_task(
        task: TaskBase,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    new_task = VkTask(user_id=user.id, **task.model_dump())
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    create_task(VkTaskCreate.model_validate(new_task), user.vk_token, VkSend)
    return VkTaskRead.model_validate(new_task)


@router.get('/vk/{pk}', response_model=VkTaskRead)
async def get_task(
        pk: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    task = await get_task_by_pk(db, user, pk)
    return task


@router.get('/vk', response_model=list[VkTaskRead])
async def get_task(
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    task_query = await db.execute(select(VkTask).where(VkTask.user_id == user.id))
    tasks = task_query.scalars().all()
    await check_task(tasks)
    return tasks


@router.delete('/vk/{pk}', status_code=status.HTTP_204_NO_CONTENT)
async def kill_vk_task(
        pk: int,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    task = await get_task_by_pk(db, user, pk)
    kill_task(task.id)
    await db.delete(task)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


async def get_task_by_pk(db: AsyncSession, user: User, pk: int) -> VkTask:
    task_query = await db.execute(select(VkTask).where(VkTask.id == pk))
    task = task_query.first()
    await check_task(task, pk)
    task = task[0]
    if task.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Not authorized to perform action'
        )
    return task


async def check_task(task, pk: int | None = None):
    if pk:
        detail = f'vk_task with id {pk} not found'
    else:
        detail = f'vk_tasks not found'

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )


