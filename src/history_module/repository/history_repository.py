from history_module.repository.abstract_history_repository import (
    AbstractHistoryRepository,
)


class HistoryRepository(AbstractHistoryRepository):
    def __init__(self, db):
        self.db = db
