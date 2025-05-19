from flask import Blueprint, jsonify, request
from src.access_module.services.login import Login
from typing import List
from src.access_module.models.user import User


class LoginController:
    def __init__(self):
        self.login_bp = Blueprint("login", __name__, url_prefix="/access")
        self.login_service = Login()
        self.register_routes()

    def register_routes(self):
        self.login_bp.add_url_rule("/login", view_func=self.login, methods=["GET"])
        self.login_bp.add_url_rule("/signup", view_func=self.sign_up, methods=["POST"])
        self.login_bp.add_url_rule("/users", view_func=self.get_users, methods=["GET"])

    def login(self):  # ← Sin parámetros
        user_email = request.args.get("email")
        user_password = request.args.get("password")

        if not user_email or not user_password:
            return jsonify({"error": "Email and password are required"}), 400

        try:
            response = self.login_service.login(user_email, user_password)
            return jsonify({"result": response}), 200
        except ValueError as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def sign_up(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        try:
            result = self.login_service.sign_up(email, password)
            return jsonify({"result": result}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def get_users(self):
        users: List[User] = self.login_service.get_users()
        return jsonify([user.to_dict() for user in users])


# Para usar el blueprint:
login_controller = LoginController()
login_bp = login_controller.login_bp
