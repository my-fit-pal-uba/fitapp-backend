from abc import abstractmethod


class AbstractRegistrationService:
    """
    Abstract class for registration services.
    """

    @abstractmethod  # noqa: F821
    def register_progile(self, profile_type: str, user_id: int):
        """
        Register a new user.

        :param user_data: Dictionary containing user data.
        :return: Registration result.
        """
        raise NotImplementedError("Subclasses must implement this method.")
