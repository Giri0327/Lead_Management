from sqlalchemy.ext.declarative import declarative_base
from session import engine
Base= declarative_base()



if __name__==__name__:
    Base.metadata.create_all(bind=engine)