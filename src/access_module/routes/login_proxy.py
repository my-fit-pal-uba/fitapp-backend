from flask import Blueprint, request

from access_module.routes.login_controller import LoginController
from models.response import ResponseInfo


### Aca agrego la logica dependiente de flasl
class LoginProxy:
    def __init__(self, login_controller: LoginController):
        self.login_controller: LoginController = login_controller
        self.login_bp = Blueprint("login", __name__, url_prefix="/access")
        self.register_routes()

    def register_routes(self):
        self.login_bp.add_url_rule("/login", view_func=self.login, methods=["GET"])
        # self.login_bp.add_url_rule("/signup", view_func=self.sign_up, methods=["POST"])
        # self.login_bp.add_url_rule("/users", view_func=self.get_users, methods=["GET"])

    def login(self):
        data = request.args.to_dict()
        user_email = data.get("email", None)
        user_password = data.get("password", None)
        if not user_email or not user_password:
            return ResponseInfo.to_response(
                (False, "Email and password are required", 400)
            )

        responde = self.login_controller.login(user_email, user_password)

        return ResponseInfo.to_response(responde)

    def sign_up(self):
        pass
