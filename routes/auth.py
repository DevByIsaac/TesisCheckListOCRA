from flask import Blueprint, request, jsonify
from .database import SessionLocal
from .crud import create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    db = SessionLocal()
    user = create_user(db, username, password, email)
    db.close()
    
    if user:
        return jsonify({"msg": "User registered successfully"}), 201
    return jsonify({"msg": "User registration failed"}), 400
