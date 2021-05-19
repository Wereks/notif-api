from hashlib import sha1

from fastapi import FastAPI, Depends, HTTPException, Path, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def conpath_id():
    return Path(..., gt=0, title="ID of the message", description="Positive integer, to specify which message we want to target", example=13)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(password: str, hashed_password: str):
    return hashed_password == sha1(password.encode(encoding='UTF-8')).hexdigest()

def authenticate_user(db: Session, username: str, password: str):
    """Returns False if user with those credentials doesnt exists, else returns the user"""
    user = crud.get_user(db, schemas.User(username=username))
    print(username, password, user)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def get_db_authorized(user = Depends(oauth2_scheme)):
    yield from get_db()  

def message_not_none(message):
    """Checks if message is None (if doesnt exists)"""
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message 

@app.post("/token", description="Endpoint used for authorization")
async def authorization(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/messages/{id}", response_model=schemas.Message, description="Returns the message specified by the id")
def read_message(id: int = conpath_id(), db: Session = Depends(get_db)):
    message = crud.read_message(db, id)
    return message_not_none(message)

@app.post("/messages/", response_model=schemas.Message)
def create_message(text: schemas.MessageCreate = Body(..., examples=schemas.MessageCreate._examples), db: Session = Depends(get_db_authorized)):
    message = crud.create_message(db, text)
    print(text)
    return message

@app.put("/messages/{id}", response_model=schemas.Message, description="Updates the text of message specified by the id, resets views to 0")
def update_message_text(text: schemas.MessageCreate, id: int = conpath_id(), db: Session = Depends(get_db_authorized)):
    message = crud.update_message_text(db, id, text)
    return message_not_none(message)

@app.delete("/messages/{id}", response_model=schemas.Message, description="Returns and delete from the database the message specified by the id")
def delete_message(id: int = conpath_id(), db: Session = Depends(get_db_authorized)):
    message = crud.delete_message(db, id)
    return message_not_none(message)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Message Board",
        version="1.0.0",
        description="API which gives access to reading, creating, updating, deleting messages saved on the server.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi







