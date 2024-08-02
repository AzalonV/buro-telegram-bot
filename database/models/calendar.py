from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from database.models.base import Base

class Calendar(Base):
    __tablename__ = 'Calendar'

    id = Column(Integer, unique=True, autoincrement=True, primary_key=True)
    group = Column(String)
    day = Column(String)
    num = Column(String)
    lesson = Column(String)