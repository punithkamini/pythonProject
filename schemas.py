from pydantic import BaseModel
from typing import Literal
import datetime


class Task(BaseModel):
    task: str
    taskFlag: Literal["Not Done", "Done"]
    priority: Literal[1, 2, 3, 4, 5]
    deadline: datetime.datetime


class User(BaseModel):
    userId: int
    userName: str
    userPwd: str


class ShowUser(BaseModel):
    userId: int
    userName: str

    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    userId: int = None
    userName: str = None
