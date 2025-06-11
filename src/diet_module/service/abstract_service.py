from abc import abstractmethod


class AbstractDietService:

    @abstractmethod
    def get_diets(self, user_id: str) -> list:
        """
        Retrieve the diet information for a given user.

        :param user_id: The ID of the user whose diet is to be retrieved.
        :return: A dictionary containing the user's diet information.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def create_diet(self, user_id: str, diet_data: dict) -> dict:
        """
        Create a new diet for a user.

        :param user_id: The ID of the user for whom the diet is to be created.
        :param diet_data: A dictionary containing the diet data.
        :return: The created diet object.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def add_dish(self, diet_id: str, dish_data: dict) -> dict:
        """
        Add a dish to a specific diet.
        :param diet_id: The ID of the diet to which the dish will be added.
        :param dish_data: A dictionary containing the dish data.
        :return: The updated diet object with the added dish.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
