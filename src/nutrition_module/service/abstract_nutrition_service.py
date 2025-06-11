from abc import abstractmethod

from nutrition_module.models.dish import dish
from nutrition_module.models.dish_consumption import DishConsumption


class AbstractNutritionService:

    @abstractmethod
    def get_meal_categories(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def post_dish(self, dish: dish):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_dishes(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def post_dish_consumption(self, dish_consumption: DishConsumption):
        raise NotImplementedError("This method should be overridden by subclasses")
