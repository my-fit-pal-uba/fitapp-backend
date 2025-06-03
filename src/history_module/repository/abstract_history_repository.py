from abc import abstractmethod


class AbstractHistoryRepository:

    @abstractmethod
    def get_calories_history(self):
        """
        Fetches the calories history.
        :return: List of dictionaries with date and calories.
        """
        pass
