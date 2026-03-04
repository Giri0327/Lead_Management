from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

dburl=""
engine=create_engine(dburl)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# from dotenv import load_dotenv
# import os

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
