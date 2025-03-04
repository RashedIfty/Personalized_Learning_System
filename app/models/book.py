from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey
from app.core.database import Base
from datetime import datetime

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, nullable=False)
    text_content = Column(String, nullable=False)
    embedding = Column(LargeBinary, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # NEW: Associates book with a user
