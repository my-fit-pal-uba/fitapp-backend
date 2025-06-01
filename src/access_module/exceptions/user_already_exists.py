class UserAlreadyExists(Exception):
    """Exception raised when a user already exists in the system."""

    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email {email} already exists.")
