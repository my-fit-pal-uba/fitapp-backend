from history_module.repository.abstract_history_repository import (
    AbstractHistoryRepository,
)

from typing import Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore  # noqa: F401


class HistoryRepository(AbstractHistoryRepository):
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

    def get_calories_history(self, user_id: int):
        query = """
            SELECT
            DATE(date) AS day,
            SUM(calories) AS total_calories
            FROM calories_history
            WHERE user_id = %s
            GROUP BY DATE(date) 
            ORDER BY day
            lIMIT 50
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id,))
                records = cursor.fetchall()
                return list(
                    map(
                        lambda record: {
                            "date": str(record["day"]),
                            "calories": (
                                float(record["total_calories"])
                                if record["total_calories"] is not None
                                else 0.0
                            ),
                        },
                        records,
                    )
                )
        except psycopg2.Error:
            return []

    def get_weight_history(self, user_id: int):
        query = """
            SELECT
            DATE(date) AS day,
            AVG(weight) AS avg_weight
            FROM weight_history
            WHERE user_id = %s
            GROUP BY DATE(date) 
            ORDER BY day DESC
            LIMIT 50
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id,))
                records = cursor.fetchall()
                return list(
                    map(
                        lambda record: {
                            "date": str(record["day"]),
                            "weight": (
                                float(record["avg_weight"])
                                if record["avg_weight"] is not None
                                else 0.0
                            ),
                        },
                        records,
                    )
                )
        except psycopg2.Error:
            return []
