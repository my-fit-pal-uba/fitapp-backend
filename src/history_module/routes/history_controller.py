from history_module.services.abstract_history_service import AbstractHistoryService


class HistoryController:

    def __init__(self, history_service: AbstractHistoryService):
        self.history_service: AbstractHistoryService = history_service

    def get_calories_history(self):
        try:
            calories_history = self.history_service.get_calories_history()
            return calories_history, "Success", 200
        except Exception:
            return [], "An error has ocurred", 500
