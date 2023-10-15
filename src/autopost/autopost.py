from celery import Celery, schedules
from redbeat import RedBeatSchedulerEntry
from abc import ABC, abstractmethod
from typing import Type

import requests

from schemas.task import TaskBase
from config import settings

redbeat_redis_url = f'redis://{settings.redis_hostname}:{settings.redis_port}'
celery = Celery('tasks', broker=redbeat_redis_url)
redbeat_lock_key = None
beat_max_loop_interval=5
redbeat_lock_timeout=10
celery.autodiscover_tasks(force=True)


class Send(ABC):
    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    @abstractmethod
    def send(self, params: dict):
        raise NotImplementedError


class VkSend(Send):
    name = 'VkSend.send'

    @staticmethod
    @celery.task(name=name)
    def send(params: dict):
        res = requests.get('https://api.vk.com/method/messages.send', params=params)
        return res.status_code


def create_task(task: TaskBase, access_token: str, send: Type[Send]) -> str:
    params = task.model_dump(exclude={'user_id', 'is_active', 'delay'}, by_alias=True)
    params.update({'access_token': access_token})
    interval = schedules.schedule(run_every=task.delay)
    entry = RedBeatSchedulerEntry(
        task.__repr__(),
        send.name,
        interval,
        args=[params],
        app=celery
    )
    entry.save()
    return entry.key


def kill_task(task_id: int) -> None:
    key = f'redbeat:VkTask {task_id}'
    RedBeatSchedulerEntry.from_key(key=key, app=celery).delete()
