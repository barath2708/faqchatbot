from sqlalchemy import Column, Integer, String, DateTime, func

from app.database import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    status = Column(String, default="pending")  # pending, success, failed
    chunks_created = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())