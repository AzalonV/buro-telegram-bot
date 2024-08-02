from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from database.models.base import Base

class Event(Base):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True, unique=True)
    text = Column(String)
    photo = Column(String)
    time = Column(String)
    date = Column(String)
    date_time = Column(DateTime)