from pydantic import BaseModel, Field, field_validator

import requests

from schemas.task import TaskBase


class VkToken(BaseModel):
    token: str

    @field_validator('token')
    @classmethod
    def validate_token(cls, token: str) -> str:
        params = {'access_token': token, 'v': '5.131'}
        res = requests.get('https://api.vk.com/method/users.get', params=params)
        if 'error' in res.text:
            raise ValueError('token is invalid')
        return token


class VkTaskRead(TaskBase):
    id: int
    user_id: int
    chat_id: int = Field(serialization_alias='peer_id')
    is_active: bool = True


class VkTaskCreate(VkTaskRead):
    random_id: int = 0
    v: str = '5.131'

    def __repr__(self):
        return f'VkTask {self.id}'

    class Config:
        from_attributes = True
