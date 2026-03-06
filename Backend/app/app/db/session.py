from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
# url="mysql+pymysql://4WUWyWmxdkEPJB7.root:BSGkzQO4R1Vb1R5O@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/Lead_Management"
# #DATABASE_URL=url

# # get current file directory
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # go one folder up to find .env
# env_path = os.path.join(BASE_DIR, "..", ".env")

# load_dotenv(env_path)
cert_path = os.getenv("ca")

#print("DATABASE_URL:", DATABASE_URL)
#print("CA:", cert_path)

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