from abc import abstractmethod


class AbstractHistoryRepository:

    @abstractmethod
    def get_calories_history(self, user_id: int):
        """
        Fetches the calories history.
        :return: List of dictionaries with date and calories.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_weight_history(self, user_id: int):
        """
        Fetches the weight history.
        :return: List of dictionaries with date and weight.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
