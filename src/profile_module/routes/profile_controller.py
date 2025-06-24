from profile_module.services.abstract_profile_service import AbstractProfileService
from models.profile import Profile
from models.user import User
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pytz import timezone
import jwt

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))


class ProfileController:
    def __init__(self, profile_service: AbstractProfileService):
        self.ProfileService: AbstractProfileService = profile_service

    def get_user_by_id(self, user_id: int):
        return self.ProfileService.get_user_by_id(user_id)

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

    def register_user_rol_with_token(self, user_id: int, rol_id: int):
        success, data, status = self.register_user_rol(user_id, rol_id)
        if not success:
            return False, data, status

        user = self.get_user_by_id(user_id)
        if not user:
            return False, {"error": "User not found"}, 404

        token = self.create_access_token(user)

        return (
            True,
            {"message": "User role registered successfully", "token": token},
            200,
        )

    def register_user_rol(self, user_id: int, rol_id: int) -> tuple:
        if not user_id or not rol_id:
            return False, {"error": "User ID and role are required"}, 400

        result = self.ProfileService.register_rol(rol_id, user_id)
        if result is None:
            return False, {"error": "Failed to register user role"}, 500

        if not result:
            return False, {"error": "An error has ocurred"}, 400
        return True, {"message": "User role registered successfully"}, 200

    def post_photo(self, user_id: int, photo: bytes) -> tuple:
        if not user_id or not photo:
            return False, {"error": "User ID and photo are required"}, 400

        if not photo.startswith(b"\x89PNG\r\n\x1a\n"):
            return False, {"error": "Only PNG files are allowed"}, 400

        result = self.ProfileService.post_photo(user_id, photo)
        if not result:
            return False, {"error": "Failed to post photo"}, 500

        return True, {"message": "Photo posted successfully"}, 200

    def get_photos(self, user_id: int) -> list:
        return self.ProfileService.get_photos(user_id)

    def get_code(self, user_id: int) -> tuple:
        return self.ProfileService.get_code(user_id)

    def create_access_token(self, user: User):
        dict_user = user.to_dict()
        to_encode = dict_user.copy()
        expire = datetime.now() + timedelta(minutes=JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        argentina_time = datetime.now(
            timezone("America/Argentina/Buenos_Aires")
        ).isoformat()
        to_encode.update({"access_time": argentina_time})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt
