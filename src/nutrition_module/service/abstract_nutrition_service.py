from abc import abstractmethod


class AbstractNutritionService:

    @abstractmethod
    def get_meal_categories(self):
        raise NotImplementedError("This method should be overridden by subclasses")
