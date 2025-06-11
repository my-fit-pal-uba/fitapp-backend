from diet_module.service.abstract_service import AbstractDietService
from typing import Tuple


class DietController:
    def __init__(self, diet_service: AbstractDietService):
        self.diet_service: AbstractDietService = diet_service

    def get_diets(self, user_id):
        diets = self.diet_service.get_diets(user_id)

        if not diets:
            return False, {"message": "There are no diets"}, 404

        return True, diets, 200

    def create_diet(self, user_id, diet_data) -> Tuple[bool, dict, int]:
        if not user_id or not diet_data:
            return False, {"message": "User ID and diet data are required"}, 400

        diet = self.diet_service.create_diet(user_id, diet_data)

        if not diet:
            return False, {"message": "Failed to create diet"}, 500

        return True, diet, 201

    def add_dish(self, diet_id, dish_data) -> Tuple[bool, dict, int]:
        if not diet_id or not dish_data:
            return False, {"message": "Diet ID and dish data are required"}, 400

        dish = self.diet_service.add_dish(diet_id, dish_data)

        if not dish:
            return False, {"message": "Failed to add dish to diet"}, 500

        return True, dish, 201
