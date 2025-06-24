from history_module.repository.abstract_history_repository import (
    AbstractHistoryRepository,
)
from routine_module.repository.routine_repository import RoutineRepository
from history_module.model.consumption_history import consumption_history  # noqa: F401
from typing import Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore  # noqa: F401


class HistoryRepository(AbstractHistoryRepository):
    def __init__(self, db_config=None):
        self.routine_repository = RoutineRepository()
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
            ORDER BY day
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

    def get_routine_history(self, user_id: int) -> list:
        query = """
            SELECT * 
            FROM done_routines 
            WHERE user_id = %s 
            ORDER BY done_at DESC
            LIMIT 50
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id,))
                records = cursor.fetchall()
                result = []
                for record in records:
                    routine = self.routine_repository.get_routine_by_id(
                        record["routine_id"]
                    )
                    result.append(
                        {
                            "done_at": str(record["done_at"])[:10],
                            "routine": routine,  # Aquí devuelves la rutina completa
                        }
                    )
                return result
        except psycopg2.Error:
            return []

    def get_routine_history_by_date(self, user_id: int, done_at: str) -> list:
        query = """
            SELECT * 
            FROM done_routines 
            WHERE user_id = %s AND DATE(done_at) = %s
            ORDER BY done_at DESC
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id, done_at))
                records = cursor.fetchall()
                result = []
                for record in records:
                    routine = self.routine_repository.get_routine_by_id(
                        record["routine_id"]
                    )
                    result.append(
                        {"done_at": str(record["done_at"])[:10], "routine": routine}
                    )
                return result
        except psycopg2.Error:
            return []

    def _map_record_to_daily_consumption(self, record):
        return consumption_history(
            fecha_consumo=str(record["fecha_consumo"]),
            total_calorias=(
                float(record["total_calorias"]) if record["total_calorias"] else 0.0
            ),
            total_proteinas=(
                float(record["total_proteinas"]) if record["total_proteinas"] else 0.0
            ),
            total_carbohidratos=(
                float(record["total_carbohidratos"])
                if record["total_carbohidratos"]
                else 0.0
            ),
            total_grasas=(
                float(record["total_grasas"]) if record["total_grasas"] else 0.0
            ),
        )

    def get_all_history(self, user_id: int) -> list:
        query = """
            SELECT 
                DATE(consumption_date) AS fecha_consumo,
                ROUND(SUM(calories)::numeric, 2) AS total_calorias,
                ROUND(SUM(protein)::numeric, 2) AS total_proteinas,
                ROUND(SUM(carbohydrates)::numeric, 2) AS total_carbohidratos,
                ROUND(SUM(fats)::numeric, 2) AS total_grasas
            FROM 
                dishes_history 
            WHERE 
                user_id = %s
            GROUP BY 
                DATE(consumption_date)
            ORDER BY 
                fecha_consumo DESC
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id,))
                records = cursor.fetchall()
                if not records:
                    return []
                return [
                    self._map_record_to_daily_consumption(record) for record in records
                ]
        except psycopg2.Error as e:
            print("Error fetching all history:", e)
            return []
