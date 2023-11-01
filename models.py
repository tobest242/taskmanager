from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


Base = declarative_base()

class User(UserMixin, Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(100))

    def get_id(self):
        return str(self.user_id)
    

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    attachments = Column(String(255))