class AbstractHistoryService:

    def get_calories_history(self, user_id: int):
        """
        Retrieves the weight history.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
