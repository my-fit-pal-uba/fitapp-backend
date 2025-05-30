from access_module.services.abstract_login import AbstractAccessService
from typing import Tuple

from access_module.exceptions.invalid_password import InvalidUserPassword
from access_module.exceptions.non_existing_user import NonExistingUser


class LoginController:
    def __init__(self, login_service: AbstractAccessService):
        self.login_service: AbstractAccessService = login_service

    def login(self, user_email: str, user_password: str) -> Tuple[bool, str, int]:

        if not user_email or not user_password:
            return False, "Email and password are required", 400

        try:
            response = self.login_service.login(user_email, user_password)
            return response, "Login successful", 200
        except NonExistingUser:
            return False, "User does not exist", 404
        except InvalidUserPassword:
            return False, "Invalid password", 404
