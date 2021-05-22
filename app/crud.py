from sqlalchemy.orm import Session

from .models import Message, User
from . import schemas

def read_message(db: Session, message_id: int):
    req = Message.__table__.update().\
            where(Message.id == message_id).\
            values(views=Message.views + 1).\
            returning(Message)        
    msg = db.execute(req).first()
    db.commit()

    if msg:
        msg = schemas.Message(**msg)
        msg.views = msg.views - 1

    return msg

def read_messages(db: Session, skip: int = 0, limit: int = 100):    
    messages = db.execute(Message.__table__.select().order_by(Message.id).offset(skip).limit(limit)).fetchall()

    if messages:
        min_id, max_id = messages[0].id, messages[-1].id
        req = Message.__table__.update().\
                where(Message.id >= min_id, Message.id <= max_id).\
                values(views=Message.views + 1)
        db.execute(req)
        db.commit()

    return messages

def create_message(db: Session, message: schemas.MessageCreate):
    db_message = Message(text=message.text)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

    return db_message
   
def update_message_text(db: Session, message_id: int, message: schemas.MessageCreate):
    req = Message.__table__.update().\
            where(Message.id == message_id).\
            values(views=0, text=message.text).\
            returning(Message)
    msg = db.execute(req).first()
    db.commit()
    return msg

def delete_message(db: Session, message_id: int):
    req = Message.__table__.delete().\
            where(Message.id == message_id).\
            returning(Message)
    msg = db.execute(req).first()
    db.commit()
    return msg


def get_user(db: Session, user: schemas.User):
    return db.query(User).filter(User.username == user.username).first()
