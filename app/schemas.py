from pydantic import BaseModel, Field, field_validator, EmailStr

import requests


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


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


class UserRead(UserBase):
    id: int


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(UserBase):
    ...


class TaskBase(BaseModel):
    chat_id: int
    delay: int
    message: str

    class Config:
        from_attributes = True


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


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int
