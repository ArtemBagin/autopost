from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, Boolean

from database import Base


class User(Base):
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password = Column(String(length=1024), nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    vk_token = Column(String, unique=True, default='')


class VkTask(Base):
    __tablename__ = 'vk_task'

    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    chat_id = Column(Integer, nullable=False)
    delay = Column(Integer, nullable=False)
    message = Column(String(length=4096), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

