from nutrition_module.service.abstract_nutrition_service import AbstractNutritionService
from nutrition_module.models.dish import dish


class NutritionController:
    def __init__(self, nutrition_service: AbstractNutritionService):
        self.nutrition_service: AbstractNutritionService = nutrition_service

    def get_meal_categories(self):
        try:
            meals_categories = self.nutrition_service.get_meal_categories()
            return True, [meal.to_dict() for meal in meals_categories], 200
        except Exception as e:
            print(f"Error fetching meal categories: {e}")
            return False, [], 500

    def post_dish(self, dish_json: dict):
        try:
            dish_data = dish.from_dict(dish_json)
            if not dish_data.is_valid():
                return False, "Invalid dish data", 500
            result = self.nutrition_service.post_dish(dish_data)
            print(result)
            return True, dish_data.to_dict(), 200
        except Exception as e:
            print(f"Error registering dish: {e}")
            return False, str(e), 500
