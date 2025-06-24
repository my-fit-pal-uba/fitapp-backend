from abc import abstractmethod


class AbstractAccessService:
    """
    An abstract base class that defines the interface for access services,
    such as login and logout functionality. Subclasses should implement
    the 'login' and 'logout' methods to provide concrete authentication logic.

    Methods
    -------
    login(username: str, password: str) -> bool
        Abstract method for authenticating a user with the given username and password.
        Should return True if authentication is successful, False otherwise.

    logout() -> None
        Abstract method for logging out the current user.
    """

    @abstractmethod
    def login(self, username: str, password: str) -> str:
        """
        Abstract method to be implemented by subclasses for user login.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def logout(self) -> None:
        """
        Abstract method to be implemented by subclasses for user logout.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def sign_up(self, email: str, password: str, name: str, last_name: str) -> str:
        """
        Abstract method to be implemented by subclasses for user sign-up.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def sign_up_google(self, idinfo) -> str:
        """
        Abstract method to be implemented by subclasses for user sign-up-google.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def login_google(self, idinfo) -> str:
        """
        Abstract method to be implemented by subclasses for user login.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def restore_password_mail(self, user_email: str) -> str:
        """
        Abstract method to be implemented by subclasses for restoring password via email.
        """
        raise NotImplementedError("Subclasses should implement this method.")
