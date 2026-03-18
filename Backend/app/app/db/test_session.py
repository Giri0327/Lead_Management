# test_session.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base
from app.main import app
from app.api.deps import get_db


DATABASE_TEST_URL = os.getenv("DATABASE_TEST_URL")  
CERT_PATH = os.getenv("ca")  


engine = create_engine(
    DATABASE_TEST_URL,
    connect_args={"ssl": {"ca": CERT_PATH}},  # must match TiDB Cloud requirement
    pool_pre_ping=True
)

# ✅ Create tables in test DB
Base.metadata.create_all(bind=engine)

# ✅ Session factory for tests
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ✅ Dependency override for FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()  # commit all changes
    finally:
        db.close()

# ✅ Apply dependency override
app.dependency_overrides[get_db] = override_get_db