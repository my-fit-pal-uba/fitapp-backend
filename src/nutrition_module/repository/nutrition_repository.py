from datetime import datetime
from nutrition_module.repository.abstract_nutrition_repository import (
    AbstractNutritionRepository,
)

from typing import List, Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore

from nutrition_module.models.meal_categorie import MealCategory
from nutrition_module.models.dish import dish
from nutrition_module.models.dish_equivalences import DishEquivalences  # type: ignore
import os
from urllib.parse import urlparse


class NutritionRepository(AbstractNutritionRepository):
    """
    Repository for managing nutrition-related data.
    This class extends the AbstractRepository to provide specific methods for nutrition data.
    """

    def __init__(self, db_config=None):
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            result = urlparse(database_url)
            self.db_config = {
                "host": result.hostname,
                "database": result.path.lstrip("/"),
                "user": result.username,
                "password": result.password,
                "port": result.port or 5432,
            }
        else:
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

    def post_dish_categories(
        self, dish_id: int, category_ids: list[int]
    ) -> list[int] | None:
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
                inserted_ids = []
                for category_id in category_ids:
                    cursor.execute(
                        query,
                        (dish_id, category_id),
                    )
                    result = cursor.fetchone()
                    if result:
                        inserted_ids.append(result["id"])

                conn.commit()
                return inserted_ids if inserted_ids else None

        except psycopg2.Error as e:
            print(f"Error al insertar categorías: {e}")
            return None

    def _map_dish_record_to_dish(self, records):
        dishes_dict = {}
        for record in records:
            dish_id = record["id"]
            if dish_id not in dishes_dict:
                dishes_dict[dish_id] = dish(
                    id=record["id"],
                    name=record["name"],
                    description=record["description"],
                    calories=record["calories"],
                    proteins=record["proteins"],
                    carbs=record["carbs"],
                    fats=record["fat"],
                    weight=record["weight_in_g"],
                    id_dish_category=[record["category_id"]],
                )
            else:
                dishes_dict[dish_id].id_dish_category.append(record["category_id"])
        return list(dishes_dict.values())

    def get_dishes(self):
        query = """
            SELECT 
            dish.id,
            dish.name, 
            dish.description, 
            dish.calories, 
            dish.proteins, 
            dish.carbs, 
            dish.fat, 
            dish.weight_in_g, 
            dish_ca.category_id
            FROM dishes AS dish
            INNER JOIN dish_categories AS dish_ca
            ON dish.id = dish_ca.dish_id 
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(query, ())
                records = cursor.fetchall()
                return self._map_dish_record_to_dish(records)
        except psycopg2.Error as e:
            print(f"Error al insertar categorías: {e}")
            return None

    def get_dish_by_id(self, dish_id: int) -> Optional[dish]:
        query = """
            select 
                dish.id,
                dish.name, 
                dish.description, 
                dish.calories, 
                dish.proteins, 
                dish.carbs, 
                dish.fat, 
                dish.weight_in_g, 
                dish_ca.category_id
            from dishes as dish
            inner join dish_categories as dish_ca
            on dish.id = dish_ca.dish_id 
            where dish.id = %s
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(query, (dish_id,))
                record = cursor.fetchone()
                if record:
                    return self._map_dish_record_to_dish([record])[0]
                return None
        except psycopg2.Error as e:
            print(f"Error fetching dish by ID: {e}")
            return None

    def post_dish_consumption(
        self, dish_id: int, user_id: int, equivalencies: DishEquivalences
    ) -> bool:
        query = """
            INSERT INTO dishes_history (
                user_id,
                dish_id,
                serving_size_g,
                calories,
                protein,
                carbohydrates,
                fats
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s
            );
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(
                    query,
                    (
                        user_id,
                        dish_id,
                        equivalencies.weight,
                        equivalencies.calories,
                        equivalencies.protein,
                        equivalencies.carbohydrates,
                        equivalencies.fats,
                    ),
                )
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Error registering dish consumption: {e}")
            return False

    def post_calories_history(self, user_id: int, calories: float) -> tuple:
        query = """
            INSERT INTO calories_history (user_id, date, calories)
            VALUES (%s, %s, %s);
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (user_id, datetime.now(), calories),
                )
                conn.commit()
                return True
        except psycopg2.Error:
            print("Error al registrar las calorias")
            return False
