from abc import abstractmethod

from models.profile import Profile


class AbstractProfileService:
    """
    Abstract class for Profile services.
    """

    @abstractmethod
    def register_rol(self, rol: str, user_id: int) -> tuple:
        """
        Register a new role for a user.

        :param rol: The role to be registered.
        :param user_id: The ID of the user.
        :return: A tuple containing the result of the operation.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def register_daily_weight(self, user_id: int, weight: float) -> tuple:
        """
        Register the daily weight of a user.

        :param user_id: The ID of the user.
        :param weight: The weight to be registered.
        :return: A tuple containing the result of the operation.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def register_daily_calories(self, user_id: int, calories: float) -> tuple:
        """
        Register the daily calories of a user.

        :param user_id: The ID of the user.
        :param calories: The calories to be registered.
        :return: A tuple containing the result of the operation.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def save_profile(self, profile: Profile) -> tuple:
        """
        Save a user's profile.

        :param profile: The profile data to be saved.
        :return: A tuple containing the result of the operation.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def get_profile(self, user_id: int) -> tuple:
        """
        Retrieve a user's profile.

        :param user_id: The ID of the user.
        :return: A tuple containing the profile data.
        """
        raise NotImplementedError("Subclasses must implement this method.")
