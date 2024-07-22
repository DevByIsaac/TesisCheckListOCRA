import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:12345@localhost/tesis-checklist-ocra'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'lonuestroesunsecreto'
