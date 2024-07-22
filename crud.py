from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from .models import User

def create_user(db: Session, username: str, password: str, email: str):
    hashed_password = generate_password_hash(password, method='sha256')
    db_user = User(username=username, password_hash=hashed_password, email=email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
