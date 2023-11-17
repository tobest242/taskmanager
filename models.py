from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

# user mode
class User(UserMixin, Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    name = Column(String(100))
    created_tasks = relationship("Task", back_populates="user", foreign_keys="[Task.user_email]")
    assigned_tasks = relationship("Task", back_populates="assigned_to_user", foreign_keys="[Task.assigned_to_user_email]")

    
    def get_id(self):
        return str(self.user_id)


# task model
class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    due_date = Column(DateTime)
    user_email = Column(String(100), ForeignKey('users.email'), nullable=False)
    assigned_to_user_email = Column(String(100), ForeignKey('users.email'))
    user = relationship("User", back_populates="created_tasks", foreign_keys=[user_email])
    assigned_to_user = relationship("User", back_populates="assigned_tasks", foreign_keys=[assigned_to_user_email])