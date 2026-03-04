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
