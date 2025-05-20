class InvalidUserPassword(Exception):
    """Exception raised for invalid password errors."""

    def __init__(self, message="Invalid password provided."):
        self.message = message
        super().__init__(self.message)
