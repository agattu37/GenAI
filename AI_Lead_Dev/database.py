import os
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class LeadEmail(Base):
    __tablename__ = 'lead_emails'

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String, unique=True, index=True)
    sender = Column(String, index=True)
    subject = Column(Text)
    body = Column(Text)
    received_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='new', index=True)

    intent = Column(String, nullable=True)
    is_sales_lead = Column(Boolean, nullable=True)
    summary = Column(Text, nullable=True)


def create_tables():

    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully")


if __name__== "__main__":
    create_tables()
