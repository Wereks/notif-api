from typing import Annotated, Dict
from pydantic import BaseModel, Field


class MessageBase(BaseModel):
    text: Annotated[str, Field(
        min_length=1, max_length=160, title="Text of the message")]


class MessageCreate(MessageBase):
    _examples: Dict = {
        "normal": {
            "summary": "A normal example",
            "description": "Text between 1 and 160 chars, works perfectly",
            "value": {
                "text": "First message in examples",
            },
        },
        "empty": {
            "summary": "Example with text which is too short",
            "description": "Message cannot be created from an empty text",
            "value": {
                "text": "",
            },
        },
        "too_long": {
            "summary": "Example with text which is too long",
            "description": "Message cannot be created from an text longer than 160 characters",
            "value": {
                "text": "0123456789"*16 + "0",
            },
        },
    }

    class Config:
        title = 'Message needed to create a new one'
        description = 'The bare minimum what a message needs to be saved in the database'

        schema_extra = {"example": {"text": "Example message"}}


class Message(MessageBase):
    id: Annotated[int, Field(
        gt=0, title="ID used to determine a specific message")]
    views: Annotated[int, Field(
        ge=0, title="How many times was the message viewed")]

    class Config:
        orm_mode = True
        title = 'Message saved in the database'
        description = 'Schema of the message including all the informations, id, views and text'

        schema_extra = {
            'example': {
                "text": "Example message",
                "id": 12,
                "views": 9,
            },
        }


class User(BaseModel):
    username: str


class UserInDB(User):
    hashed_password: str
