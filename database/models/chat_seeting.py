from sqlalchemy import Column, Integer, Boolean, DateTime, func

from database.models.base import Base

class ChatSetting(Base):
    __tablename__ = 'ChatSetting'

    chat_id = Column(Integer, primary_key=True)
    is_mailing = Column(Boolean, default=True)