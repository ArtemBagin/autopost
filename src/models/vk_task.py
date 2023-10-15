from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import Boolean

from database.database import Base


class VkTask(Base):
    __tablename__ = 'vk_task'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, nullable=False)
    delay: Mapped[int] = mapped_column(Integer, nullable=False)
    message: Mapped[str] = mapped_column(String(length=4096), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

