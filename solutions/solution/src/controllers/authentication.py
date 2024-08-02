# solutions/solution/src/controllers/auth.py

from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify, abort
from flask_jwt_extended import create_access_token
from solutions.solution.src.models.user import User
from flask import current_app

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    repo = current_app.repository
    user = next((u for u in repo.get_all(User) if u.email == email), None)
    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token, user_id=user.id), 200
    return jsonify({"msg": "Bad email or password"}), 401


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({"msg": "Logout successful"})
    response.set_cookie('jwt_token', '', expires=0)
    response.set_cookie('user_id', '', expires=0)
    return response
