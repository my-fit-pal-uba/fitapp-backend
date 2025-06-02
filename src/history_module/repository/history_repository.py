from history_module.repository.abstract_history_repository import (
    AbstractHistoryRepository,
)


class HistoryRepository(AbstractHistoryRepository):
    def __init__(self, db_config=None):
        self.db_config = db_config or {
            "host": "db",
            "database": "app_db",
            "user": "app_user",
            "password": "app_password",
            "port": "5432",
        }
