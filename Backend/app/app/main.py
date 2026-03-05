#from db.session import *
from app.db.session import engine
from app.db.base_class import Base
from app.api.endpoints import users,password
import app.models
import app.api
from app.api.endpoints import users
from app.api.endpoints import lead
from fastapi import FastAPI
app = FastAPI()

app.include_router(users.router)
app.include_router(password.router)
app.include_router(lead.router)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)  