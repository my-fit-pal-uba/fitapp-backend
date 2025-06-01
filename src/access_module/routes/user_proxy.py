from flask import Blueprint, request

from access_module.routes.user_controller import UserController
from models.response import ResponseInfo


class UserProxy:
    def __init__(self, user_controller: UserController):
        self.user_controller = user_controller
        self.user_bp = Blueprint("user", __name__, url_prefix="/users")
        self.register_routes()

    def register_routes(self):
        pass
