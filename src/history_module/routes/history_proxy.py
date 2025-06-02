from history_module.routes.history_controller import HistoryController


class HistoryProxy:
    def __init__(self, history_controller: HistoryController):
        self.history_service: HistoryController = history_controller
