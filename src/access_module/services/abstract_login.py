class AbstractLogin:
    def login(self, username: str, password: str) -> bool:
        """
        Abstract method to be implemented by subclasses for user login.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    def logout(self) -> None:
        """
        Abstract method to be implemented by subclasses for user logout.
        """
        raise NotImplementedError("Subclasses should implement this method.")
