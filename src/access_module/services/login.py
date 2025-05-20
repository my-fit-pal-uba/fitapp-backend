from access_module.models.user import User
from access_module.repository.abstract_access_repository import AbstractAccessRepository
from access_module.exceptions.non_existing_user import NonExistingUser

from access_module.services.abstract_login import AbstractAccessService
from access_module.exceptions.invalid_password import InvalidUserPassword
from access_module.exceptions.user_already_exists import UserAlreadyExists


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

    def sign_up(self, email: str, password: str, name: str, last_name: str):
        try:
            result = self.repository.create_user(email, password, name, last_name)
            if not result:
                raise UserAlreadyExists(email)
            return True
        except Exception:
            return False

    def get_users(self):
        return self.repository.get_users()
