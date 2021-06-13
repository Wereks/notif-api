from sqlalchemy import Column, Integer, String  # type: ignore

from .database import Base, engine


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(160))
    views = Column(Integer, default=0)


class User(Base):
    __tablename__ = "users"

    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String)


Base.metadata.create_all(bind=engine)
