from fastapi import HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession

from autopost.autopost import VkSend, create_task, kill_task
from models.user import User
from models.vk_task import VkTask
from repositories.user import UserRepository
from repositories.vk_task import VkTaskRepository
from schemas.task import TaskBase
from schemas.vk import VkToken, VkTaskCreate, VkTaskRead


async def add_vk_token(
        token: VkToken,
        user: User,
        db: AsyncSession
):
    await UserRepository(db).edit_one(id=user.id, data={'vk_token': token.token})
    return {'status': 'token successfully changed'}


async def check_and_get_task(db: AsyncSession, user: User, pk: int) -> VkTask:
    task = await VkTaskRepository(db).find_one(id=pk)
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


async def get_tasks(
        user: User,
        db: AsyncSession,
):
    tasks = await VkTaskRepository(db).find(user_id=user.id)
    await check_task(tasks)
    return tasks


async def create_vk_task(
        task: TaskBase,
        user: User,
        db: AsyncSession,
):
    data = task.model_dump()
    data.update({'user_id': user.id})
    new_task = await VkTaskRepository(db).add_one(data)
    create_task(VkTaskCreate.model_validate(new_task), user.vk_token, VkSend)
    return VkTaskRead.model_validate(new_task)


async def kill_vk_task(
        pk: int,
        user: User,
        db: AsyncSession,
):
    task = await check_and_get_task(db, user, pk)
    await db.delete(task)
    await db.commit()
    kill_task(task.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
