from abc import abstractmethod

from nutrition_module.models.dish import dish


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
