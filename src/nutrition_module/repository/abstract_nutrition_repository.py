from abc import abstractmethod

from nutrition_module.models.dish_equivalences import DishEquivalences


class AbstractNutritionRepository:

    @abstractmethod
    def get_meal_categories(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def post_dish(self, dish):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def post_dish_category(self, dish):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_dishes(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_dish_by_id(self, dish_id: int):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def post_dish_consumption(
        self, dish_id: int, user_id: int, equivalencies: DishEquivalences
    ):
        raise NotImplementedError("This method should be overridden by subclasses")
