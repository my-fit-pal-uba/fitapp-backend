from abc import abstractmethod


class AbstractHistoryService:

    def get_calories_history(self, user_id: int):
        """
        Retrieves the weight history.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def get_weight_history(self, user_id: int):
        """
        Retrieves the weight history.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def get_routine_history(self, user_id: int) -> list:
        """
        Retrieves the routine history.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def get_routine_history_by_date(self, user_id: int, date: str) -> list:
        """
        Retrieves the routine history for a specific date.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
