from pydantic import BaseModel, Field, constr


class MessageBase(BaseModel):
    text: constr(min_length=1, max_length=160)

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int = Field(..., ge=0)
    views: int = Field(..., ge=0)

    class Config:
        orm_mode = True