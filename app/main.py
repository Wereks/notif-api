from fastapi import FastAPI, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session  # type: ignore

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check(message):
    """Checks if message is None (exists)"""
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message 


@app.get("/messages/{id}", response_model=schemas.Message)
def get_message(id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    message = crud.get_message(db, id)
    return check(message)

@app.post("/messages/", response_model=schemas.Message)
def create_message(text: schemas.MessageCreate, db: Session = Depends(get_db)):
    print(text)
    message = crud.create_message(db, text)
    return message

@app.put("/messages/{id}", response_model=schemas.Message)
def update_message_text(text: schemas.MessageCreate, id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    message = crud.update_message_text(db, id, text)
    return check(message)

@app.delete("/messages/{id}", response_model=schemas.Message)
def delete_message(id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    message = crud.delete_message(db, id)
    return check(message)








