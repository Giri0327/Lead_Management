from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

dburl="mysql://4WUWyWmxdkEPJB7.root:BSGkzQO4R1Vb1R5O@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/Lead_Management"
engine = create_engine(dburl,
    connect_args={
        "ssl": {
            "ca": "path/to/ca-cert.pem"
        }
    }
)

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
