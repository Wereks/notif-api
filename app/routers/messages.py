from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Body, Query
from sqlalchemy.orm import Session

from ..dependencies import get_db, get_db_authorized
from ..schemas import Message, MessageCreate
from .. import crud

router = APIRouter()


def conpath_id():
    return Path(..., gt=0, title="ID of the message", description="Positive integer, to specify which message we want to target", example=17)


def exists(message):
    """Checks if message is None (if doesnt exists)"""
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")

    return message


@router.get("/{id}", response_model=Message,
            description="Returns the message specified by the id, the view counter includes the current view of the message")
def read_message(id: int = conpath_id(), db: Session = Depends(get_db)):
    message = crud.read_message(db, id)
    return exists(message)


@router.get("/", response_model=List[Message],
            description="Returns a list of messages, each of them is specified by read_message definition")
def read_messages(db: Session = Depends(get_db),
                  skip: int = Query(
                      0, ge=0, description="Number of messages to skip"),
                  limit: int = Query(100, ge=1, le=100, description="Number of messages to be shown")):
    messages = crud.read_messages(db, skip, limit)
    return messages


@router.post("/", response_model=Message,
             description="Creates a new message from text, returning the saved message in the database")
def create_message(text: MessageCreate = Body(..., examples=MessageCreate._examples), db: Session = Depends(get_db_authorized)):
    message = crud.create_message(db, text)
    return message


@router.put("/{id}", response_model=Message,
            description="Updates the text of message specified by the id, resets views to 0, returns message state after the update")
def update_message_text(text: MessageCreate, id: int = conpath_id(), db: Session = Depends(get_db_authorized)):
    message = crud.update_message_text(db, id, text)
    return exists(message)


@router.delete("/{id}", response_model=Message,
               description="Deletes the message specified by the id from the database, returns the message before the delete")
def delete_message(id: int = conpath_id(), db: Session = Depends(get_db_authorized)):
    message = crud.delete_message(db, id)
    return exists(message)
