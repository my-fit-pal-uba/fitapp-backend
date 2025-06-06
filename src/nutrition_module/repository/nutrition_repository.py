from nutrition_module.repository.abstract_nutrition_repository import (
    AbstractNutritionRepository,
)

from typing import List, Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor

from nutrition_module.models.meal_categorie import MealCategory  # type: ignore


class NutritionRepository(AbstractNutritionRepository):
    """
    Repository for managing nutrition-related data.
    This class extends the AbstractRepository to provide specific methods for nutrition data.
    """

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

    def get_meal_categories(self, user_id: int) -> List[MealCategory]:
        query = """
            SELECT 
            id,
            description
            FROM meal_categories
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(query, ())
                records = cursor.fetchall()
                return [
                    MealCategory(id=record["id"], description=record["description"])
                    for record in records
                ]
        except psycopg2.Error:
            return []
