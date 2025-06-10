from history_module.services.abstract_history_service import AbstractHistoryService
from history_module.repository.abstract_history_repository import (
    AbstractHistoryRepository,
)


class HistoryService(AbstractHistoryService):

    def __init__(self, abstract_history_repository):
        self.history_repository: AbstractHistoryRepository = abstract_history_repository

    def get_calories_history(self, user_id: int):
        try:
            calories_history = self.history_repository.get_calories_history(user_id)
            return calories_history
        except Exception:
            return []

    def get_weight_history(self, user_id: int):
        try:
            weight_history = self.history_repository.get_weight_history(user_id)
            return weight_history
        except Exception:
            return []

    def get_routine_history(self, user_id: int) -> list:
        if not user_id:
            return []
        routine_history = self.history_repository.get_routine_history(user_id)
        return routine_history

    def get_routine_history_by_date(self, user_id: int, date: str) -> list:
        if not user_id or not date:
            return []

        routine_history = self.history_repository.get_routine_history_by_date(
            user_id, date
        )
        return routine_history
