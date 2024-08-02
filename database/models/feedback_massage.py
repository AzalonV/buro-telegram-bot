from sqlalchemy import Column, Integer, String, DateTime, func

from database.models.base import Base

class FeedbackMessage(Base):
    __tablename__ = 'Message'

    message_id = Column(Integer, primary_key=True)
    from_user_message_id = Column(Integer)
    message_time = Column(DateTime, default=func.now())
    user_id = Column(Integer)