from flask import request, jsonify

from . import bp
from app.models import User
from app.blueprints.api.helpers import token_required

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
            "username": user.username,
            "first_name": user.first_name,
            "token": user.token
        }])
    elif user and not user.check_password(password):
        return jsonify([{
        "message": "Password incorrect.",
        "error": "password",
        "success": False
    }])
    return jsonify([{
        "message": "User info not found.",
        "error": "user",
        "success": False
    }])

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
        "username": user.username,
        "token": user.token
    }])

# Get User Information
@bp.route('/get-user/<username>', methods=["GET"])
@token_required
def get_user(user, username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify([{
            "username": username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name
        }])
    return jsonify({
        "message": "User info not found.",
        "success": False
    })

@bp.route('/update-account', methods=["PUT"])
@token_required
def update_account(user):
    updateUser = User.query.filter_by(token=user.token).first()
    content = request.json
    first_name = content['first_name']
    last_name = content['last_name']
    username = content['username']
    email = content['email']
    if updateUser:

        user_check = User.query.filter(User.token != user.token).all()
        print(user_check)
        if updateUser.username != username and username not in user_check:
            return jsonify([{
                "message": "Username is taken. Try again.",
                "success": False
            }])
        email_check = User.query.filter_by(email=email).first()
        if updateUser.email != email and not email_check:
            return jsonify([{
                "message": "Email is already registered. Try again.",
                "success": False
            }])
        updateUser.first_name = first_name
        updateUser.last_name = last_name
        updateUser.email = email
        updateUser.username = username
        updateUser.commit()
        return jsonify([{
            "message": f"{updateUser.username} successfully updated!",
            "success": True,
            "first_name": updateUser.first_name,
            "last_name": updateUser.last_name,
            "username": updateUser.username,
            "email": updateUser.email
        }])
    return jsonify([{
            "message": "Update not successful. Try logging in again.",
            "success": False
        }])