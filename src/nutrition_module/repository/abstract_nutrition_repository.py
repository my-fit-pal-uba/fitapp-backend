from abc import abstractmethod


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

    def get_dishes(self):
        raise NotImplementedError("This method should be overridden by subclasses")
