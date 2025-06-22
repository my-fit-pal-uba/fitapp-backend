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

    @abstractmethod
    def get_routine_history(self, user_id: int) -> list:
        """
        Fetches the routine history.
        :return: List of dictionaries with date and routine details.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def get_routine_history_by_date(self, user_id: int, date: str) -> list:
        """
        Fetches the routine history for a specific date.
        :return: List of dictionaries with routine details for the specified date.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def get_all_history(self, user_id: int) -> list:
        """
        Fetches all history for a user.
        :return: List of dictionaries with all history details.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
