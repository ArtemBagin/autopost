from pydantic import BaseModel, EmailStr


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


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'
    expires_in: int
