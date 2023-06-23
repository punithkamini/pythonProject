from sqlalchemy import Column, String, Integer, DateTime,ForeignKey
from db_connections import Base
from sqlalchemy.orm import relationship


class Tasks(Base):
    __tablename__="tasks"

    taskId = Column(Integer, primary_key=True)
    ownerId = Column(Integer, ForeignKey('users.userId'),nullable=False)
    tasks = Column(String, nullable=False)
    taskFlag= Column(String, nullable=False)
    priority=Column(Integer, nullable=False)
    deadline=Column(DateTime, nullable=False)
    owner=relationship("Users", back_populates="task")


class Users(Base):
    __tablename__="users"

    userId = Column(Integer, primary_key=True)
    userName = Column(String, nullable=False)
    userPwd = Column(String, nullable=False)
    task=relationship("Tasks", back_populates="owner")
