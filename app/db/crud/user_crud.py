from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext

# Setup password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_username(db: Session, username: str) -> User:
    """Retrieve a user by username."""
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str) -> User:
    """Create a new user with a hashed password."""
    hashed_password = pwd_context.hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def verify_user_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed version."""
    return pwd_context.verify(plain_password, hashed_password)
