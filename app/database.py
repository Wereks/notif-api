import os

from sqlalchemy import create_engine  # type: ignore
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy.orm import sessionmaker  # type: ignore

from .ev import *

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
    SQLALCHEMY_DATABASE_URI = 'postgresql' + SQLALCHEMY_DATABASE_URI[8::]

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
