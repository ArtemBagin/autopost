from repositories.repository import SQLAlchemyRepository

from models.user import User


class UserRepository(SQLAlchemyRepository):
    model = User

