class AbstractHistoryService:

    def get_calories_history(self):
        """
        Retrieves the weight history.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
