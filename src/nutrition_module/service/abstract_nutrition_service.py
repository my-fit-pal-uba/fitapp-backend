from abc import abstractmethod


class AbstractNutritionService:

    @abstractmethod
    def get(self):
        raise NotImplementedError("This method should be overridden by subclasses")
