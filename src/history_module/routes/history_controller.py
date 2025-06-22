from history_module.services.abstract_history_service import AbstractHistoryService
from typing import Tuple


class HistoryController:

    def __init__(self, history_service: AbstractHistoryService):
        self.history_service: AbstractHistoryService = history_service

    def get_calories_history(self, user_id: int):
        try:
            calories_history = self.history_service.get_calories_history(user_id)
            return calories_history, "Success", 200
        except Exception:
            return [], "An error has ocurred", 500

    def get_weight_history(self, user_id: int):
        try:
            weight_history = self.history_service.get_weight_history(user_id)
            return weight_history, "Success", 200
        except Exception:
            return [], "An error has ocurred", 500

    def get_routine_history(self, user_id: int) -> Tuple[bool, dict, int]:
        if not user_id:
            return False, {"error": "User ID is required"}, 400
        try:
            routine_history = self.history_service.get_routine_history(user_id)
            if not routine_history:
                return False, {"error": "No routine history found"}, 404
            return True, {"routine_history": routine_history}, 200
        except Exception as e:
            return False, {"error": str(e)}, 500

    def get_routine_history_by_date(
        self, user_id: int, date: str
    ) -> Tuple[bool, dict, int]:
        if not user_id or not date:
            return False, {"error": "User ID and date are required"}, 400
        try:
            routine_history = self.history_service.get_routine_history_by_date(
                user_id, date
            )
            if not routine_history:
                return (
                    False,
                    {"error": "No routine history found for the specified date"},
                    404,
                )
            return True, {"routine_history": routine_history}, 200
        except Exception as e:
            return False, {"error": str(e)}, 500

    def get_all_history(self, user_id: int) -> Tuple[bool, dict, int]:
        if not user_id:
            return False, {"error": "User ID is required"}, 400
        try:
            all_history = self.history_service.get_all_history(user_id)
            if not all_history:
                print("No history found for user ID:", user_id)
                return False, {"error": "No history found"}, 404
            return True, [history.to_dict() for history in all_history], 200
        except Exception as e:
            return False, {"error": str(e)}, 500
