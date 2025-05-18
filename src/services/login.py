# import ..repository/access_repository
from src.models.user import User
from src.repository.access_repository import AccessRepository
import hashlib


class Login:

    def __init__(self):
        self.repository = AccessRepository()

    def say_hello(self):
        return "Hello from Login service 4"

    def login(self, user_email: str, user_password: str):
        user_data: User = self.repository.get_user_by_email(user_email)
        if not user_data:
            raise ValueError("User not found")
        # Hashear la contraseña recibida antes de comparar
        password_hash = hashlib.sha256(user_password.encode()).hexdigest()
        if password_hash != user_data.password_hash:
            raise ValueError("Invalid password")
        return "User logged in successfully"

    def sign_up(self, email: str, password: str):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        # user_id y username como None (o puedes pedir username en el registro)
        user = User(email=email, password_hash=password_hash)
        self.repository.create_user(user)
        return "User signed up successfully"

    def get_users(self):
        return self.repository.get_users()
