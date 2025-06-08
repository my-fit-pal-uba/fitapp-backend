from nutrition_module.service.abstract_nutrition_service import AbstractNutritionService
from nutrition_module.repository.abstract_nutrition_repository import (
    AbstractNutritionRepository,
)
from nutrition_module.models import dish
from typing import *  # noqa: F403

from nutrition_module.models.meal_categorie import MealCategory
from nutrition_module.exceptions.already_existing_dish import AlreadyExistingDish
from nutrition_module.models.dish_consumption import DishConsumption
from nutrition_module.models.dish_equivalences import DishEquivalences  # type: ignore # noqa: F403


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

    def get_dishes(self):
        try:
            return self.nutrition_repository.get_dishes()
        except Exception as e:
            print(f"Error fetching dishes: {e}")
            return []

    def post_dish_consumption(self, dish_consumption: DishConsumption):
        try:
            dish = self.nutrition_repository.get_dish_by_id(dish_consumption.dish_id)
            if not dish:
                print(f"Dish with ID {dish_consumption.dish_id} not found")
                return False
            equivalencies: DishEquivalences = self._calc_equivalencies(
                dish_consumption, dish
            )
            result = self.nutrition_repository.post_dish_consumption(
                dish_id=dish_consumption.dish_id,
                user_id=dish_consumption.user_id,
                equivalencies=equivalencies,
            )
            return result
        except Exception as e:
            print(f"Error registering dish consumption: {e}")
            return False

    def _calc_equivalencies(self, dish_consumption: DishConsumption, dish: dish):
        return DishEquivalences.to_equivalences(
            dish_consumption=dish_consumption, dish=dish
        )

    def post_dish_history(self, dish):
        pass

    def register_calories_history(self, calories):
        ## To do: ref to history service
        return ""
