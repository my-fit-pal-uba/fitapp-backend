from access_module.models.user import User
from access_module.repository.abstract_access_repository import AbstractAccessRepository
from access_module.exceptions.non_existing_user import NonExistingUser

from access_module.services.abstract_login import AbstractAccessService
from access_module.exceptions.invalid_password import InvalidUserPassword


class Login(AbstractAccessService):

    def __init__(self, abstract_access_service: AbstractAccessRepository):
        self.repository: AbstractAccessRepository = abstract_access_service

    def login(self, user_email: str, user_password: str):

        user_data: User = self.repository.get_user_by_email(user_email)

        if not user_data:
            raise NonExistingUser(user_email)

        if user_data.password_hash != user_password:
            raise InvalidUserPassword(user_email)

        return True

    def sign_up(self, email: str, password: str):
        # password_hash = hashlib.sha256(password.encode()).hexdigest()
        # user_id y username como None (o puedes pedir username en el registro)
        # user = User(email=email, password_hash=password_hash)
        # self.repository.create_user(user)
        return "User signed up successfully"

    def get_users(self):
        return self.repository.get_users()
