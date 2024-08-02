from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from database.models.base import Base

class User(Base):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    user_role = Column(String, default = "user")
    group = Column(String, default = "None")
    is_member_buro = Column(Boolean, default=False)
    is_senior_student = Column(Boolean, default=False)
    first_activity = Column(DateTime, default=func.now())