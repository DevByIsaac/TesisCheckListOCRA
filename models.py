'''from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    state = db.Column(db.String(2), nullable=False, default='A')  # A for Active, I for Inactive
    created_at = db.Column(db.DateTime, default=datetime.date)
    updated_at = db.Column(db.DateTime, onupdate=datetime.date)
    created_by = db.Column(db.String(50), nullable=True)
    updated_by = db.Column(db.String(50), nullable=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
'''
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(Text, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey('user.id'))
    updated_by = Column(Integer, ForeignKey('user.id'))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    created_by_user = relationship('User', remote_side=[id], backref='created_users')
    updated_by_user = relationship('User', remote_side=[id], backref='updated_users')

