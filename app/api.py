from fastapi import FastAPI, Depends, HTTPException, Path, Body, status
from fastapi.security import  OAuth2PasswordRequestForm
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session

from . import crud, models, schemas, auth
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_db_authorized(user = Depends(auth.get_current_user)):
    yield from get_db()  

def conpath_id():
    return Path(..., gt=0, title="ID of the message", description="Positive integer, to specify which message we want to target", example=13)

def message_not_none(message):
    """Checks if message is None (if doesnt exists)"""
    if message is None:
        raise HTTPException(status_code=404, detail="Message not found")
    
    return message 

@app.post("/token", description="Endpoint used for authorization")
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/messages/{id}", response_model=schemas.Message, description="Returns the message specified by the id")
def read_message(id: int = conpath_id(), db: Session = Depends(get_db)):
    message = crud.read_message(db, id)
    return message_not_none(message)

@app.post("/messages/", response_model=schemas.Message, description="Creates a new message from text, which should be in the request body")
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







