#from db.session import *
from db.session import engine
from db.base_class import Base

import models


Base.metadata.create_all(bind=engine)  