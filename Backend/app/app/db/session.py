from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) #use this to get the absolute path of the current file, then navigate to the certificate
cert_path = os.path.join(BASE_DIR, "isrgrootx.pem") #use to get the absolute path of the certificate file, assuming it's in the same directory as this file
engine = create_engine(DATABASE_URL,
    connect_args={
        "ssl": {
            "ca": os.getenv("ca")  # Put real path here
        }
    },
    pool_pre_ping=True  # Recommended for cloud DB
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()



#This is to test connection to the database 
"""
from sqlalchemy import text

try:
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Database Connected:", result.fetchone())
except Exception as e:
    print("❌ Connection Failed:", e) """