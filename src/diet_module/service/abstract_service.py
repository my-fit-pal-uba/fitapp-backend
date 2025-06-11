from abc import abstractmethod


class AbstractDietService:

    @abstractmethod
    def get_diets(self, user_id: str) -> dict:
        """
        Retrieve the diet information for a given user.

        :param user_id: The ID of the user whose diet is to be retrieved.
        :return: A dictionary containing the user's diet information.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
