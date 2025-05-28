from access_module.services.abstract_login import AbstractAccessService
from typing import Tuple


class UserController:
    def __init__(self, user_service: AbstractAccessService):
        self.user_service: AbstractAccessService = user_service

    def get_user_info(self, email: str) -> Tuple[bool, dict, int]:
        if not email:
            return False, {"error": "Email is required"}, 400
        user = self.user_service.get_user_by_email(email)
        if not user:
            return False, {"error": "User not found"}, 404

        user_data = {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
        }
        return True, user_data, 200

    def save_profile(self, email, age, height, gender) -> Tuple[bool, dict, int]:
        if not email:
            return False, {"error": "Email is required"}, 400
        user = self.user_service.get_user_by_email(email)
        if not user:
            return False, {"error": "User not found"}, 404

        self.user_service.save_user_profile(user.user_id, age, height, gender)

        return True, "Profile saved up successfully", 200

    def get_profile(self, email: str) -> Tuple[bool, dict, int]:
        if not email:
            return False, {"error": "Email is required"}, 400
        user = self.user_service.get_user_by_email(email)
        if not user:
            return False, {"error": "User not found"}, 404

        profile = self.user_service.get_user_profile(user.user_id)
        if not profile:
            return {"profile": None}

        user_data = {
            "age": profile.age,
            "height": profile.height,
            "gender": profile.gender,
        }
        return True, user_data, 200
