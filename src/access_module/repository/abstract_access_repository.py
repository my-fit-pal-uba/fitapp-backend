from abc import abstractmethod


class AbstractAccessRepository:

    @abstractmethod
    def get_user_by_email(self, email: str):
        pass
