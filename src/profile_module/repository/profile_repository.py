from profile_module.repository.abstract_profile_repository import (
    AbstractProfileRepository,
)
from typing import Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore

from models.user import User  # noqa: F401
from models.profile import Profile
from profile_module.models.user_rol import Rol  # type: ignore


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

    def _record_to_profile(self, record) -> Profile:
        return Profile(
            user_id=record["user_id"],
            age=record["age"],
            height=record["height"],
            gender=record["gender"],
        )

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

    def save_profile(self, profile: Profile) -> bool:
        query = """
            INSERT INTO profiles (user_id, age, height, gender)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id)
            DO UPDATE SET age = EXCLUDED.age, height = EXCLUDED.height, gender = EXCLUDED.gender;
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (profile.user_id, profile.age, profile.height, profile.gender),
                )
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Error al guardar perfil: {e}")
            return False

    def get_profile(self, user_id: int) -> Optional[Profile]:
        query = """
            SELECT 
                user_id, age, height, gender
            FROM profiles
            WHERE user_id = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id,))
                record = cursor.fetchone()
                return self._record_to_profile(record) if record else None

        except psycopg2.Error:
            return None

    def _record_to_rol(record):
        return Rol(
            id=record["Id"],
            resource_key=record["rol_resource_key"],
            name=record["display_name"],
            description=record["description"],
            icon=record["icon"],
        )

    def get_user_rols(self):
        query = """
            SELECT 
                Id,
                rol_resource_key,
                display_name, 
                description, 
                icon
            FROM rols
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(
                    query,
                )
                records = cursor.fetchall()
                return records if records else []
        except psycopg2.Error:
            return []

    def post_user_rol(self, user_id: int, rol_id: int) -> bool:
        query = """
            INSERT INTO user_rols (user_id, rol_id)
            VALUES (%s, %s)
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id, rol_id))
                cursor.fetchone()
                return True
        except psycopg2.Error:
            return False
