from profile_module.services.abstract_registration_service import (
    AbstractRegistrationService,
)
from profile_module.repository.abstract_repository import AbstractRegistrationRepository


class RegistrationServic(AbstractRegistrationService):

    def __init__(self, repository: AbstractRegistrationRepository):
        self.repository: AbstractRegistrationService = repository

    def register_user(self, user_data):
        # Logic to register a new user
        pass

    def verify_user(self, user_id):
        # Logic to verify a user's registration
        pass

    def update_user_info(self, user_id, updated_data):
        # Logic to update user information
        pass

    def delete_user(self, user_id):
        # Logic to delete a user
        pass
