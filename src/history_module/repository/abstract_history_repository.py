from abc import abstractmethod


class AbstractHistoryRepository:

    @abstractmethod
    def get_calories_history(self, user_id: int):
        """
        Fetches the calories history.
        :return: List of dictionaries with date and calories.
        """
        pass
