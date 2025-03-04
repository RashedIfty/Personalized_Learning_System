from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Load the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database.db")

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base model
Base = declarative_base()

# Initialize the database
def init_db():
    from app.models import book, history, user  # Ensure all models are imported
    Base.metadata.create_all(bind=engine)

# Function to get a new session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
