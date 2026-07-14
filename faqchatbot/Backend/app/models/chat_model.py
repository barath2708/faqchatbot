from sqlalchemy import Column, Integer, Text, DateTime, func

from app.database import Base


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    source_urls = Column(Text)  # comma-separated citation URLs
    created_at = Column(DateTime, server_default=func.now())