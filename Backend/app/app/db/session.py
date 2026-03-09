from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")

cert_path = os.getenv("ca")

engine = create_engine(DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": cert_path
        }
    },
    pool_pre_ping=True,pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()