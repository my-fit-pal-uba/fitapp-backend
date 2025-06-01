from datetime import datetime, timedelta
import os

from dotenv import load_dotenv
import jwt
from src.models.user import User
from access_module.repository.abstract_access_repository import AbstractAccessRepository
from access_module.exceptions.non_existing_user import NonExistingUser

from access_module.services.abstract_login import AbstractAccessService
from access_module.exceptions.invalid_password import InvalidUserPassword
from access_module.exceptions.user_already_exists import UserAlreadyExists


load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))


class Login(AbstractAccessService):

    def __init__(self, abstract_access_service: AbstractAccessRepository):
        self.repository: AbstractAccessRepository = abstract_access_service

    def login(self, user_email: str, user_password: str):

        user_data: User = self.repository.get_user_by_email(user_email)

        if not user_data:
            raise NonExistingUser(user_email)

        if user_data.password_hash != user_password:
            raise InvalidUserPassword(user_email)

        return self.create_access_token(user_data)

    def sign_up(self, email: str, password: str, name: str, last_name: str):
        result = self.repository.create_user(email, password, name, last_name)
        if not result:
            raise UserAlreadyExists(email)
        user_data: User = self.repository.get_user_by_email(email)
        return self.create_access_token(user_data)

    def create_access_token(self, user: User):
        dict_user = user.to_dict()
        to_encode = dict_user.copy()
        expire = datetime.now() + timedelta(minutes=JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def get_users(self):
        return self.repository.get_users()
