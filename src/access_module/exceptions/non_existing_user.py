class NonExistingUser(Exception):
    """Exception raised when a user does not exist in the system."""

    def __init__(self, username: str):
        self.username = username
        super().__init__(f"User with email'{self.username}' does not exist.")
