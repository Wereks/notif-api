from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from .routers import messages, authorization

app = FastAPI(        
        title="Message Board",
        version="1.5.0",
        description="API which gives access to reading, creating, updating, deleting messages saved on the server."\
                    "Every message is equipped with a view counter, which increase everytime someone reads the message",
)

app.include_router(
    messages.router,
    prefix="/messages",
    tags=["messages"]
)
app.include_router(authorization.router)