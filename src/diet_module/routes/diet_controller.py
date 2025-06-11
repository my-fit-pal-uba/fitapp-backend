from diet_module.service.abstract_service import AbstractDietService


class DietController:
    def __init__(self, diet_service: AbstractDietService):
        self.diet_service: AbstractDietService = diet_service

    def get_diets(self, user_id):
        try:
            diets = self.diet_service.get_diets(user_id)
            return True, diets, 200
        except Exception as e:
            print(f"Error retrieving diets: {e}")
            return False, [], 500
