from flask import request, jsonify

from . import bp
from app.models import User

# Verify User

@bp.route('/verify-user', methods=["POST"])
def verify_user():
    content = request.json
    username = content['username']
    password = content['password']
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return jsonify([{
            "message": f"{user.username} successfully verified!",
            "success": True,
            "first_name": user.first_name,
            "token": user.token
        }])
    return jsonify({
        "message": "User info not found.",
        "success": False
    })

# Register User

@bp.route('/register-user', methods=["POST"])
def register_user():
    content = request.json
    username = content['username']
    email = content['email']
    password = content['password']
    first_name = content['first_name']
    last_name = content['last_name']
    user_check = User.query.filter_by(username=username).first()
    if user_check:
        return jsonify([{
            "message": "Username is taken. Try again.",
            "success": False
        }])
    email_check = User.query.filter_by(email=email).first()
    if email_check:
        return jsonify([{
            "message": "Email is already registered. Try again.",
            "success": False
        }])
    user = User(email=email, username=username,
                first_name=first_name, last_name=last_name)
    user.password = user.hash_password(password)
    user.add_token()
    user.commit()
    return jsonify([{
        "message": f"{user.username} successfully registered!",
        "success": True,
        "first_name": user.first_name,
        "token": user.token
    }])
