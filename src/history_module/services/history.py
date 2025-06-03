from datetime import datetime, timedelta
import random
from history_module.services.abstract_history_service import AbstractHistoryService
from history_module.repository.abstract_history_repository import (
    AbstractHistoryRepository,
)


class HistoryService(AbstractHistoryService):

    def __init__(self, abstract_history_repository):
        self.history_repository: AbstractHistoryRepository = abstract_history_repository

    def get_calories_history(self):
        try:
            today = datetime.now()
            history = []
            for i in range(100):
                day = today - timedelta(days=i)
                calories = round(random.uniform(1500, 3000), 2)
                history.append({"date": day.strftime("%Y-%m-%d"), "calories": calories})
            grouped = {}
            for entry in history:
                date_key = entry["date"]
                if date_key not in grouped:
                    grouped[date_key] = entry
                else:
                    grouped[date_key]["calories"] += entry["calories"]
            history = list(grouped.values())
            history.sort(key=lambda x: x["date"])
            return history[::-1]
        except Exception:
            return []
