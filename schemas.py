import datetime

from pydantic import BaseModel


class FriendBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    birthdate: datetime.date


class FriendCreate(FriendBase):
    pass


class Friend(FriendBase):
    id: int

    class Config:
        orm_mode = True
