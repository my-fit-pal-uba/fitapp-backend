from datetime import datetime
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

    def _record_to_user(self, record) -> User:
        return User(
            user_id=record["user_id"],
            username=record["username"],
            email=record["email"],
            first_name=record["first_name"],
            last_name=record["last_name"],
            is_active=record["is_active"],
            is_superuser=record.get("is_admin"),
            last_login=record.get("last_login"),
            password_hash=record.get("password_hash"),
            rol_resource_key=record.get("rol_resource_key"),
        )

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def _record_to_profile(self, record) -> Profile:
        return Profile(
            user_id=record["user_id"],
            age=record["age"],
            height=record["height"],
            gender=record["gender"],
        )

    def register_rol(self, rol_id: int, user_id: int) -> bool:
        query = """
            INSERT INTO user_rols (user_id, rol_id)
            VALUES (%s, %s)
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id, rol_id))
                conn.commit()
                return True
        except psycopg2.Error:
            return False

    def register_daily_weight(self, user_id: int, weight: float) -> tuple:
        query = """
            INSERT INTO weight_history (user_id, date, weight)
            VALUES (%s, %s, %s);
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(
                    query,
                    (user_id, datetime.now(), weight),
                )
                conn.commit()
                return True
        except psycopg2.Error:
            print("Error al registrar las calorias")
            return False

    def register_daily_calories(self, user_id: int, calories: float) -> tuple:
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

    def _record_to_rol(self, record):
        return Rol(
            id=record[0],
            resource_key=record[1],
            name=record[2],
            description=record[3],
            icon=record[4],
        )

    def get_user_rols(self):
        query = """
            SELECT 
                id,
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
                cursor.execute(query)
                records = cursor.fetchall()
                return (
                    [
                        {
                            "rol_id": record["id"],
                            "resource_key": record["rol_resource_key"],
                            "display_name": record["display_name"],
                            "description": record["description"],
                            "icon": record["icon"],
                        }
                        for record in records
                    ]
                    if records
                    else []
                )
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []

    def post_photo(self, user_id: int, photo: bytes) -> tuple:
        query = """
            INSERT INTO user_photos (user_id, photo)
            VALUES (%s, %s)
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (user_id, photo))
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Error al guardar la foto: {e}")
            return False

    def get_photos(self, user_id: int) -> list:
        query = """
            SELECT photo, upload_date
            FROM user_photos
            WHERE user_id = %s
            ORDER BY upload_date ASC
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (user_id,))
                return cursor.fetchall()  # list of (photo_bytes, upload_date)
        except psycopg2.Error as e:
            print(f"Error al obtener las fotos: {e}")
            return []

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        query = """
            SELECT 
                u.user_id, u.username, u.email, u.first_name, u.last_name, 
                u.is_active, u.is_admin, u.last_login, u.password_hash, r.rol_resource_key
            FROM Users u
            JOIN user_rols ur ON u.user_id = ur.user_id
            JOIN rols r ON ur.rol_id = r.id
            WHERE u.user_id = %s;
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (user_id,))
                record = cursor.fetchone()
                return self._record_to_user(record) if record else None
        except psycopg2.Error:
            return None

    def get_code(self, user_id: int) -> tuple:
        query = """
            SELECT first_name, last_name, user_id
            FROM users
            WHERE user_id = %s;
        """
        try:
            with self.get_connection() as conn, conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute(query, (user_id,))
                record = cursor.fetchone()
                if record:
                    first_name = record['first_name'] or ""
                    last_name = record['last_name'] or ""
                    user_id = record['user_id']
                    code = f"{first_name}{last_name}#{user_id}"
                    return code
                return None
        except psycopg2.Error:
            return None
