from history_module.services.abstract_history_service import AbstractHistoryService
from history_module.repository.abstract_history_repository import (
    AbstractHistoryRepository,
)


class HistoryService(AbstractHistoryService):

    def __init__(self, abstract_history_repository):
        self.history_repository: AbstractHistoryRepository = abstract_history_repository
