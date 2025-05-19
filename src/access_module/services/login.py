from access_module.models.user import User
from access_module.repository.abstract_access_repository import AbstractAccessRepository
import hashlib

from access_module.services.abstract_login import AbstractAccessService


class Login(AbstractAccessService):

    def __init__(self, abstract_access_service: AbstractAccessRepository):
        self.repository: AbstractAccessRepository = abstract_access_service

    def say_hello(self):
        return "Hello from Login service 4"

    def login(self, user_email: str, user_password: str):
        user_data: User = self.repository.get_user_by_email(user_email)
        if not user_data:
            raise ValueError("User not found")

        if user_data.password_hash != user_password:
            raise ValueError("Invalid password")
        return True

    def sign_up(self, email: str, password: str):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        # user_id y username como None (o puedes pedir username en el registro)
        user = User(email=email, password_hash=password_hash)
        self.repository.create_user(user)
        return "User signed up successfully"

    def get_users(self):
        return self.repository.get_users()
