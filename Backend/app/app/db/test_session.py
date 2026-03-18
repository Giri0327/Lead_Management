# test_session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base
from app.main import app
from app.api.deps import get_db

# (put this in .env) DATABASE_TEST_URL=mysql+pymysql://4WUWyWmxdkEPJB7.root:BSGkzQO4R1Vb1R5O@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/lead_test_db

DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL")  
CERT_PATH = os.getenv("ca")  


engine = create_engine(
    DATABASE_TEST_URL,
    connect_args={"ssl": {"ca": CERT_PATH}},  
    pool_pre_ping=True
)

Base.metadata.create_all(bind=engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()  
    finally:
        db.close()

# Apply dependency override
app.dependency_overrides[get_db] = override_get_db