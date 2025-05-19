from access_module.services.abstract_login import AbstractAccessService

# from typing import List
# from access_module.models.user import User


class LoginController:
    def __init__(self, login_service: AbstractAccessService):
        self.login_service: AbstractAccessService = login_service

    def login(self, user_email: str, user_password: str):  # ← Sin parámetros

        if not user_email or not user_password:
            return ""

        try:
            response = self.login_service.login(user_email, user_password)
            return response
        except ValueError:
            return None
        except Exception:
            return None
