from history_module.services.abstract_history_service import AbstractHistoryService


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
