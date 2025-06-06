from nutrition_module.service.abstract_nutrition_service import AbstractNutritionService


class NutritionController:
    def __init__(self, nutrition_service: AbstractNutritionService):
        self.nutrition_service: AbstractNutritionService = nutrition_service

    def get_meal_categories(self):
        try:
            meals_categories: list = self.nutrition_service.get_meal_categories()
            return True, meals_categories, 200
        except Exception as e:
            print(f"Error fetching meal categories: {e}")
            return False, [], 500
