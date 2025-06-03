from profile_module.repository.abstract_profile_repository import (
    AbstractProfileRepository,
)
from profile_module.services.abstract_profile_service import AbstractProfileService
from models.profile import Profile


class ProfileService(AbstractProfileService):

    def __init__(self, repository: AbstractProfileRepository):
        self.repository: AbstractProfileRepository = repository

    def register_rol(self, rol_id: int, user_id: int):
        """
        Register a new role for a user.

        :param user_rol: The role to be registered.
        :param user_id: The ID of the user.
        :return: A tuple containing the result of the operation.
        """
        return self.repository.register_rol(rol_id, user_id)

    def register_daily_weight(self, user_id: int, weight: float):
        """
        Register the daily weight of a user.

        :param user_id: The ID of the user.
        :param weight: The weight to be registered.
        :return: A tuple containing the result of the operation.
        """
        return self.repository.register_daily_weight(user_id, weight)

    def register_daily_calories(self, user_id: int, calories: float):
        """
        Register the daily calories of a user.

        :param user_id: The ID of the user.
        :param calories: The calories to be registered.
        :return: A tuple containing the result of the operation.
        """
        return self.repository.register_daily_calories(user_id, calories)

    def get_profile(self, user_id: int) -> Profile:
        """
        Get the profile of a user.

        :param user_id: The ID of the user.
        :return: A tuple containing the user's profile data.
        """
        return self.repository.get_profile(user_id)

    def save_profile(self, profile: Profile):
        """
        Save the profile of a user.

        :param user_id: The ID of the user.
        :return: A boolean indicating whether the profile was saved successfully.
        """
        return self.repository.save_profile(profile)

    def get_user_rols(self):
        user_rols = self.repository.get_user_rols()
        return user_rols
