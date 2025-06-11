class AlreadyExistingDish(Exception):
    """
    Exception raised when trying to add a dish that already exists in the database.
    """

    def __init__(self, dish_name: str):
        self.dish_name = dish_name
        super().__init__(f"The dish '{self.dish_name}' already exists in the database.")
