from pydantic import BaseModel


class TaskBase(BaseModel):
    chat_id: int
    delay: int
    message: str

    class Config:
        from_attributes = True
