from abc import abstractmethod


class AbstractNutritionRepository:

    @abstractmethod
    def asdasd(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def get_meal_categories(self):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def post_dish(self, dish):
        raise NotImplementedError("This method should be overridden by subclasses")

    @abstractmethod
    def post_dish_category(self, dish):
        raise NotImplementedError("This method should be overridden by subclasses")
