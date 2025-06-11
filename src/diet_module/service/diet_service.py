from diet_module.service.abstract_service import AbstractDietService


class DietService(AbstractDietService):
    """
    Concrete implementation of the AbstractDietService that provides diet-related functionalities.
    """

    def __init__(self):
        pass

    def get_diets(self, user_id: str) -> dict:
        """
        Retrieve the diet information for a given user.

        :param user_id: The ID of the user whose diet is to be retrieved.
        :return: A dictionary containing the user's diet information.
        """
        return {
            {
                "calories": 2000,
                "description": "Enfocada en el consumo de frutas, verduras, granos enteros, pescado y aceite de oliva.",
                "name": "Dieta Mediterránea",
            }
        }
