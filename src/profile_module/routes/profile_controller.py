from profile_module.services.abstract_profile_service import AbstractProfileService
from models.profile import Profile


class ProfileController:
    def __init__(self, profile_service: AbstractProfileService):
        self.ProfileService: AbstractProfileService = profile_service

    def register_rol(self, rol: str, user_id: int) -> tuple:
        if not rol or not user_id:
            return False, {"error": "Role and user ID are required"}, 400

        result = self.ProfileService.register_rol(rol, user_id)
        if not result:
            return False, {"error": "Failed to register role"}, 500

        return True, {"message": "Role registered successfully"}, 200

    def register_daily_weight(self, user_id: int, weight: float) -> tuple:
        if not user_id or not weight:
            return False, {"error": "User ID and weight are required"}, 400

        result = self.ProfileService.register_daily_weight(user_id, weight)
        if not result:
            return False, {"error": "Failed to register daily weight"}, 500

        return True, {"message": "Daily weight registered successfully"}, 200

    def register_daily_calories(self, user_id: int, calories: float) -> tuple:
        if not user_id or not calories:
            return False, {"error": "User ID and calories are required"}, 400

        result = self.ProfileService.register_daily_calories(user_id, calories)
        if not result:
            return False, {"error": "Failed to register daily calories"}, 500

        return True, {"message": "Daily calories registered successfully"}, 200

    def save_profile(self, profile: Profile) -> tuple:
        if not profile or not profile.user_id:
            return False, {"error": "User ID and profile data are required"}, 400

        result = self.ProfileService.save_profile(profile)
        if not result:
            return False, {"error": "Failed to save profile"}, 500

        return True, {"message": "Profile saved successfully"}, 200

    def get_profile(self, user_id: int) -> tuple:
        if not user_id:
            return False, {"error": "User ID is required"}, 400

        profile = self.ProfileService.get_profile(user_id)
        if not profile:
            return False, {"error": "Profile not found"}, 404

        return True, profile.to_dict(), 200

    def get_user_rols(self) -> tuple:
        rols = self.ProfileService.get_user_rols()
        return True, rols, 200

    def register_user_rol(self, user_id: int, rol_id: int) -> tuple:
        if not user_id or not rol_id:
            return False, {"error": "User ID and role are required"}, 400

        result = self.ProfileService.register_user_rol(user_id, rol_id)
        if result is None:
            return False, {"error": "Failed to register user role"}, 500

        if not result:
            return False, {"error": "An error has ocurred"}, 400
        return True, {"message": "User role registered successfully"}, 200
