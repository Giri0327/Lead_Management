#from db.session import *
from app.db.session import engine
from app.db.base_class import Base
from app.api.endpoints import users
import app.models
import app.api
from fastapi import FastAPI
app = FastAPI()

app.include_router(users.router)

Base.metadata.create_all(bind=engine)  