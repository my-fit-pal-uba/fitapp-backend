from profile_module.repository.abstract_profile_repository import (
    AbstractProfileRepository,
)
from profile_module.services.abstract_profile_service import AbstractProfileService
from models.profile import Profile
import base64


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

    def post_photo(self, user_id, photo) -> tuple:
        """
        Post a photo for a user.

        :param user_id: The ID of the user.
        :param photo: The photo to be posted.
        :return: A tuple containing the result of the operation.
        """
        return self.repository.post_photo(user_id, photo)

    def get_photos(self, user_id: int) -> list:
        rows = self.repository.get_photos(user_id)
        photos = []
        for photo_data, upload_date in rows:
            encoded = base64.b64encode(photo_data).decode("utf-8")
            photos.append({"photo": encoded, "upload_date": upload_date.isoformat()})
        return photos

    def get_user_by_id(self, user_id: int):
        return self.repository.get_user_by_id(user_id)

    def get_code(self, user_id: int) -> tuple:
        return self.repository.get_code(user_id)
