from diet_module.service.abstract_service import AbstractDietService
from diet_module.repository.abstract_diet_repository import AbstractDietRepository


class DietService(AbstractDietService):
    """
    Concrete implementation of the AbstractDietService that provides diet-related functionalities.
    """

    def __init__(self, diet_repository: AbstractDietRepository):
        self.diet_repository: AbstractDietRepository = diet_repository

    def get_diets(self, user_id: str) -> dict:
        """
        Retrieve the diet information for a given user.

        :param user_id: The ID of the user whose diet is to be retrieved.
        :return: A dictionary containing the user's diet information.
        """
        ## return self.diet_repository.get_diets(user_id)
        return {
            "calories": 2000,
            "description": "Enfocada en el consumo de frutas, verduras, granos enteros, pescado y aceite de oliva.",
            "name": "Dieta Mediterránea",
        }
