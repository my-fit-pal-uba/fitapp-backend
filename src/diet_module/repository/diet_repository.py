from diet_module.repository.abstract_diet_repository import AbstractDietRepository

from typing import List, Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore

from diet_module.models.diet import Diet

class DietRepository(AbstractDietRepository):
    """
    Repository for managing diet-related data.
    This class extends the AbstractDietRepository to provide specific methods for diet data.
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
    
    def get_diets(self):
        query = """
            SELECT 
            id,
            name,
            observation
            FROM diets
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(query, ())
                records = cursor.fetchall()
                return [Diet.from_dict(record) for record in records]
        except psycopg2.Error as e:
            print(f"Error al buscar dietas: {e}")
            return None
        
    def get_diet_by_id(self, diet_id: int) -> Optional[Diet]:
        query = """
            SELECT 
            id,
            name,
            observation
            FROM diets
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
                    return Diet.from_dict(record)
                return None
        except psycopg2.Error as e:
            print(f"Error al buscar dieta por ID: {e}")
            return None
        