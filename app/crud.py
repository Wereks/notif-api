from sqlalchemy.orm import Session  # type: ignore

from . import models, schemas

def get_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()

def read_message(db: Session, message_id: int):
    if db_message := get_message(db, message_id):
        return_message = schemas.Message(**vars(db_message))
        db_message.views = db_message.views + 1
        db.commit()
        db.refresh(db_message)
        return return_message

    return None

def get_messages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(text=message.text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message
   
def update_message_text(db: Session, message_id: int, message: schemas.MessageCreate):
    if db_message := get_message(db, message_id):
        db_message.text = message.text
        db_message.views = 0
        db.commit()
        db.refresh(db_message)
        return db_message
    
    return None

def delete_message(db: Session, message_id: int):
    if db_message := get_message(db, message_id):
        db.delete(db_message)
        db.refresh(db_message)
        return db_message

    return None

