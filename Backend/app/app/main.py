#from db.session import *
from db.session import engine
from db.base_class import Base
#hp
import models

Base.metadata.create_all(bind=engine)  