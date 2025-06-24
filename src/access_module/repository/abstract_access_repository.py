from abc import abstractmethod


class AbstractAccessRepository:

    @abstractmethod
    def get_user_by_email(self, email: str):
        pass

    @abstractmethod
    def sign_up(self, email: str, password: str, name: str, last_name: str):
        pass

    @abstractmethod
    def change_password(self, email: str, new_password: str):
        pass
