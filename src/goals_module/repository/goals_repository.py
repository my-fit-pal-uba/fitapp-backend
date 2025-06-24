from goals_module.models.goals import Goals
from typing import List

import psycopg2  # type: ignore
from goals_module.repository.abstract_goals_repository import (
    AbstractGoalsRepository,
)
import os
from urllib.parse import urlparse


class GoalsRepository(AbstractGoalsRepository):
    def __init__(self, db_config=None):
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            # Parsear la URL para obtener params
            result = urlparse(database_url)
            self.db_config = {
                "host": result.hostname,
                "database": result.path.lstrip('/'),
                "user": result.username,
                "password": result.password,
                "port": result.port or 5432,
            }
        else:
            # Config local por defecto
            self.db_config = db_config or {
                "host": "db",
                "database": "app_db",
                "user": "app_user",
                "password": "app_password",
                "port": "5432",
            }

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def save_goal(self, user_id: int, goal_value: float) -> bool:
        query = """
            INSERT INTO goal_history (user_id, goal_value)
            VALUES (%s, %s)
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (user_id, goal_value))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error al guardar el objetivo: {e}")
            return False

    def get_latest_goal(self, user_id: int) -> tuple:
        query = """
            SELECT user_id, goal_value, registered_at
            FROM goal_history
            WHERE user_id = %s
            ORDER BY registered_at DESC
            LIMIT 1
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                result = cursor.fetchone()
                if result:
                    user_id, goal_value, registered_at = result
                    return (
                        True,
                        {
                            "user_id": user_id,
                            "goal_value": goal_value,
                            "registered_at": registered_at.isoformat(),
                        },
                        200,
                    )
                else:
                    return (
                        False,
                        {"message": "No se encontró objetivo para el usuario"},
                        404,
                    )
        except Exception as e:
            return False, {"message": f"Error interno: {str(e)}"}, 500

    def get_all_goals_by_user(self, user_id: int) -> list:
        query = """
            SELECT goal_value, registered_at
            FROM goal_history
            WHERE user_id = %s
            ORDER BY registered_at ASC
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                results = cursor.fetchall()
                return [
                    {"goal_value": float(row[0]), "registered_at": row[1]}
                    for row in results
                ]
        except Exception as e:
            raise Exception(f"Error fetching goal history: {e}")
