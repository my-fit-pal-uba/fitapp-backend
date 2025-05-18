from flask import Blueprint, jsonify
from src.services.login import Login
from typing import List
from src.models.user import User

login_bp = Blueprint("login", __name__, url_prefix="/access")

login_service = Login()


@login_bp.route("/login")
def login():
    return login_service.say_hello()


@login_bp.route("/signin")
def sign_in():
    try:
        return login_service.sign_in()
    except Exception as e:
        print(e)
        return ""


@login_bp.route("/users", methods=["GET"])
def get_users():
    users: List[User] = login_service.get_users()
    return jsonify([user.to_dict() for user in users])
