from diet_module.service.abstract_service import AbstractDietService
from diet_module.repository.abstract_diet_repository import AbstractDietRepository


class DietService(AbstractDietService):
    """
    Concrete implementation of the AbstractDietService that provides diet-related functionalities.
    """

    def __init__(self, diet_repository: AbstractDietRepository):
        self.diet_repository: AbstractDietRepository = diet_repository

    def get_diets(self, user_id: str) -> list:
        """
        Retrieve the diet information for a given user.

        :param user_id: The ID of the user whose diet is to be retrieved.
        :return: A dictionary containing the user's diet information.
        """
        diets = self.diet_repository.get_diets(user_id)

        if not diets:
            return {"message": "There are no diets"}

        return [dict(diet) for diet in diets]

    def create_diet(self, user_id: str, diet_data: dict) -> dict:
        diet = self.diet_repository.create_diet(user_id, diet_data)

        if not diet:
            return {"message": "Failed to create diet"}

        return diet.to_dict()

    def add_dish(self, diet_id: str, dish_data: dict) -> dict:
        dish = self.diet_repository.add_dish(diet_id, dish_data)

        if not dish:
            return {"message": "Failed to add dish to diet"}

        return dict(dish)
