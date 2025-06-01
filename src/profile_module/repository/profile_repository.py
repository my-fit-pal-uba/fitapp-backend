from profile_module.repository.abstract_profile_repository import (
    AbstractProfileRepository,
)
from typing import Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore


class ProfileRepository(AbstractProfileRepository):

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

    def register_rol(self, rol: str, user_id: int) -> tuple:

        query = """
            INSERT INTO UserRoles (user_id, role_id)
            VALUES (%s, %s)
            RETURNING user_id, role_id
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id, rol))
                record = cursor.fetchone()
                return self._record_to_user(record) if record else None
        except psycopg2.Error:
            return None

    def register_daily_weight(self, user_id: int, weight: float) -> tuple:
        raise NotImplementedError("Subclasses must implement this method.")

    def register_daily_calories(self, user_id: int, calories: float) -> tuple:
        raise NotImplementedError("Subclasses must implement this method.")
