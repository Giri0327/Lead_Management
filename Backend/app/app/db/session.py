from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL = "mysql+pymysql://4WUWyWmxdkEPJB7.root:BSGkzQO4R1Vb1R5O@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/Lead_Management"
cert_path = os.getenv("ca") 

engine = create_engine(DATABASE_URL,
    connect_args={
        "ssl": {
            "ca":cert_path 
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