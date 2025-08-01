# =================================================================================
# Database Configuration & Session Management
# =================================================================================
# This file handles the connection to the PostgreSQL database using SQLAlchemy.
# It reads the database URL from environment variables, which is a best practice
# for keeping sensitive information out of the code.
# =================================================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load environment variables for local development (from a .env file)
# In production on EC2, these will be set as actual environment variables.
from dotenv import load_dotenv
load_dotenv()

#SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:YourSecurePassword123@localhost:5432/fastapidb")


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()