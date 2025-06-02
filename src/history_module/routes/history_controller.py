from history_module.services.abstract_history_service import AbstractHistoryService


class HistoryController:

    def __init__(self, history_service: AbstractHistoryService):
        self.history_service: AbstractHistoryService = history_service
