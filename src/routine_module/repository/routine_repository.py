from routine_module.models.routine import Routine
import psycopg2  # type: ignore
from routine_module.repository.abstract_routine_repository import AbstractRoutineRepository

class RoutineRepository(AbstractRoutineRepository):
    def __init__(self, db_config=None):
        self.db_config = db_config or {
            "host": "db",
            "database": "app_db",
            "user": "app_user",
            "password": "app_password",
            "port": "5432",
        }
    
    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def _record_to_routine(self, record) -> Routine:
        return Routine(
            routine_id=record["routine_id"],
        )