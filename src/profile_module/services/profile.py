from src.profile_module.services.abstract_profile_service import (
    AbstractRegistrationService,
)
from src.profile_module.repository.abstract_registration_repository import (
    AbstractRegistrationRepository,
)


class RegistrationServic(AbstractRegistrationService):

    def __init__(self, repository: AbstractRegistrationRepository):
        self.repository: AbstractRegistrationService = repository

    def register_rol(self, user_rol: str, user_id: int):
        """
        Register user rol
        """
        return self.repository.register_progile(user_rol, user_id)
