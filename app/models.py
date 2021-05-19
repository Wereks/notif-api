from dataclasses import dataclass

from sqlalchemy import Column, Integer, String # type: ignore

from .database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(160))
    views = Column(Integer, default=0)