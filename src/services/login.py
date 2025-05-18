# import ..repository/access_repository
from src.models.user import User
from src.repository.access_repository import AccessRepository


class Login:

    def __init__(self):
        self.repository = AccessRepository()

    def say_hello(self):
        return "Hello from Login service 4"

    def login(self, user_email: str, user_password: str):
        user_data: User = self.repository.get_user_by_email(user_email)
        if not user_data:
            raise ValueError("User not found")
        if user_password != user_data.password_hash:
            raise ValueError("Invalid password")
        return True

    def sign_in(self):
        print("Paso por aca")
        return "Hola !"

    def get_users(self):
        return self.repository.get_users()
