from profile_module.services.abstract_profile_service import AbstractProfileService


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

        result = self.ProfileService.post_daily_weight(user_id, weight)
        if not result:
            return False, {"error": "Failed to register daily weight"}, 500

        return True, {"message": "Daily weight registered successfully"}, 200

    def register_daily_calories(self, user_id: int, calories: float) -> tuple:
        if not user_id or not calories:
            return False, {"error": "User ID and calories are required"}, 400

        result = self.ProfileService.post_daily_calories(user_id, calories)
        if not result:
            return False, {"error": "Failed to register daily calories"}, 500

        return True, {"message": "Daily calories registered successfully"}, 200
