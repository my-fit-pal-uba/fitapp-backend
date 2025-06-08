from nutrition_module.service.abstract_nutrition_service import AbstractNutritionService
from nutrition_module.models.dish import dish
from nutrition_module.exceptions.already_existing_dish import AlreadyExistingDish


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
            return True, result.to_dict(), 200
        except AlreadyExistingDish:
            return False, "Dish already exists", 401
        except Exception as e:
            print(f"Error registering dish: {e}")
            return False, str(e), 500

    def get_dishes(self):
        try:
            dishes = self.nutrition_service.get_dishes()
            return True, [dish.to_dict() for dish in dishes], 200
        except Exception as e:
            print(f"Error fetching dishes: {e}")
            return False, [], 500

    def post_dish_consumption(self, dish_consumption_json: dict):
        try:
            # dish_consumption = self.nutrition_service.post_dish_consumption(dish_consumption_json)
            # return True, dish_consumption.to_dict(), 200
            return True, "Dish consumption registered successfully", 200
        except Exception as e:
            # print(f"Error registering dish consumption: {e}")
            # return False, str(e), 500
            print(f"Error registering dish consumption: {e}")
            return False, "Error registering dish consumption", 500
