
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL,echo=False,connect_args={
    "ssl": {
        "ca": "Lead-Management\Backend\app\app\isrgrootx.pem"
        }})
SessionLocal=sessionmaker(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:

        db.close()
