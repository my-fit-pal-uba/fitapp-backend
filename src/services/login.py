# import ..repository/access_repository
from src.repository.access_repository import get_users


class Login:

    def __init__(self):
        pass

    def say_hello(self):
        return "Hello from Login service 4"

    def sign_in(self):
        print("Paso por aca")
        return "Hola !"

    def get_users(self):
        return get_users()
