from nutrition_module.service.abstract_nutrition_service import AbstractNutritionService
from nutrition_module.repository.abstract_nutrition_repository import (
    AbstractNutritionRepository,
)
from nutrition_module.models import dish
from typing import *  # noqa: F403

from nutrition_module.models.meal_categorie import MealCategory
from nutrition_module.exceptions.already_existing_dish import AlreadyExistingDish  # type: ignore # noqa: F403


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
        new_id: int = self.nutrition_repository.post_dish_history(dish)
        dish.id = new_id
        if dish.id is None:
            raise AlreadyExistingDish(dish.name)
        result: list[int] = self.nutrition_repository.post_dish_categories(
            dish.id, dish.id_dish_category
        )
        if not result or len(result) != len(dish.id_dish_category):
            raise ValueError("Failed to associate dish with category")
        return dish

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
