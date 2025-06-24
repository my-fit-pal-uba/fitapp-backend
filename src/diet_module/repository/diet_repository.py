from diet_module.repository.abstract_diet_repository import AbstractDietRepository

from typing import List, Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore

from diet_module.models.diet import Diet
import os
from urllib.parse import urlparse


class DietRepository(AbstractDietRepository):
    """
    Repository for managing diet-related data.
    This class extends the AbstractDietRepository to provide specific methods for diet data.
    """

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

    def _record_to_diet(self, record) -> Diet:
        return Diet(
            id=record["id"], name=record["name"], observation=record["observation"]
        )

    def get_diets(self, user_id) -> list:
        query = """
            SELECT 
                id,
                name,
                observation
            FROM diet
        """
        dish_query = """
            SELECT 
                dd.id AS diet_dish_id,
                dd.dish_id,
                dd.diet_id,
                dd.meal_category_id,
                dd.serving_size_g,
                d.name AS dish_name,
                d.description AS dish_description,
                d.calories,
                d.proteins,
                d.carbs,
                d.fat,
                d.weight_in_g,
                mc.description AS meal_category_description
            FROM diet_dishes dd
            JOIN dishes d ON dd.dish_id = d.id
            JOIN meal_categories mc ON dd.meal_category_id = mc.id
            WHERE dd.diet_id = %s
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(query, ())
                records = cursor.fetchall()
                diets = []
                for record in records:
                    # Convertir la dieta a dict directamente
                    diet = dict(record)
                    # Obtener los platos asociados a esta dieta
                    cursor.execute(dish_query, (diet["id"],))
                    dishes = cursor.fetchall()
                    # Convertir los platos a dict
                    diet["dishes"] = [dict(dish) for dish in dishes]
                    diets.append(diet)
                return diets
        except psycopg2.Error as e:
            import traceback

            print(f"Error al buscar dietas: {e}")
            traceback.print_exc()
            return None

    def get_diet_by_id(self, diet_id: int) -> Optional[Diet]:
        query = """
            SELECT 
            id,
            name,
            observation
            FROM diet
            WHERE id = %s
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(query, (diet_id,))
                record = cursor.fetchone()
                if record:
                    return self._record_to_diet(record)
                return None
        except psycopg2.Error as e:
            print(f"Error al buscar dieta por ID: {e}")
            return None

    def create_diet(self, user_id, diet_data):
        query = """
            INSERT INTO diet (name, observation)
            VALUES (%s, %s)
            RETURNING id, name, observation
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(query, (diet_data["name"], diet_data["observation"]))
                record = cursor.fetchone()
                conn.commit()
                return self._record_to_diet(record)
        except psycopg2.Error as e:
            print(f"Error al crear dieta: {e}")
            return None

    def add_dish(self, diet_id, dish_data):
        query = """
            INSERT INTO diet_dishes (diet_id, dish_id, meal_category_id, serving_size_g)
            VALUES (%s, %s, %s, %s)
            RETURNING id, dish_id, diet_id, meal_category_id, serving_size_g
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(
                    query,
                    (
                        diet_id,
                        dish_data["dish_id"],
                        dish_data["meal_category_id"],
                        dish_data["serving_size_g"],
                    ),
                )
                record = cursor.fetchone()
                conn.commit()
                return record
        except psycopg2.Error as e:
            print(f"Error al agregar plato a la dieta: {e}")
            return None
