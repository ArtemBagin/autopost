from repositories.repository import SQLAlchemyRepository

from models.vk_task import VkTask


class VkTaskRepository(SQLAlchemyRepository):
    model = VkTask

