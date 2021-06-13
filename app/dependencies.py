import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import SessionLocal
from . import auth

TOKEN_URL = os.getenv('TOKEN_URL')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        return auth.get_current_user(db, token)
    except auth.CredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_db_authorized(user=Depends(get_current_user)):
    yield from get_db()
