from nutrition_module.service.abstract_nutrition_service import AbstractNutritionService
from nutrition_module.repository.abstract_nutrition_repository import (
    AbstractNutritionRepository,
)
from nutrition_module.models import dish
from typing import *  # noqa: F403

from nutrition_module.models.meal_categorie import MealCategory  # type: ignore # noqa: F403


class NutritionService(AbstractNutritionService):

    def __init__(self, nutrition_repository: AbstractNutritionRepository):
        self.nutrition_repository: AbstractNutritionRepository = nutrition_repository

    def get_meal_categories(self) -> List[MealCategory]:  # noqa: F405
        try:
            return self.nutrition_repository.get_meal_categories()
        except Exception as e:
            print(f"Error fetching meal categories: {e}")
            return []

    def post_dish(self, dish: dish):
        try:
            result: bool = self.nutrition_repository.post_dish_history(dish)
            return result
        except Exception as e:
            print(f"Error posting dish: {e}")
            return False

    # def register_dish(self, dish):
    #     try:
    #         return self.nutrition_repository.register_dish(dish)
    #     except Exception as e:
    #         print(f"Error registering dish: {e}")
    #         return None

    def get_dishes(self):
        try:
            return self.nutrition_repository.get_dishes()
        except Exception as e:
            print(f"Error fetching dishes: {e}")
            return []

    def post_dish_history(self, dish):
        pass

    def register_calories_history(self, calories):
        ## To do: ref to history service
        return ""
