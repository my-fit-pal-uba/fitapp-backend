from nutrition_module.repository.abstract_nutrition_repository import (
    AbstractNutritionRepository,
)

from typing import List, Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore

from nutrition_module.models.meal_categorie import MealCategory
from nutrition_module.models.dish import dish  # type: ignore


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

    def get_meal_categories(self) -> List[MealCategory]:
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

    def post_dish_history(self, dish: dish) -> bool:
        query = """
            INSERT INTO dishes (name, description, calories, proteins, carbs, fat, weight_in_g)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(
                    query,
                    (
                        dish.name,
                        dish.description,
                        dish.calories,
                        dish.proteins,
                        dish.carbs,
                        dish.fats,
                        dish.weight,
                    ),
                )
                new_id = cursor.fetchone()["id"]
                conn.commit()
                return new_id
        except psycopg2.Error:
            return None

    def post_dish_category(self, dish_id: int, category_id: int) -> bool:

        query = """
            INSERT INTO dish_categories (dish_id, category_id)
            VALUES (%s, %s)
            RETURNING id
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(
                    query,
                    (
                        dish_id,
                        category_id,
                    ),
                )
                new_id = cursor.fetchone()["id"]
                conn.commit()
                return new_id
        except psycopg2.Error:
            return None
