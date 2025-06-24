from typing import Optional
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore
from models.user import User
from models.profile import Profile  # noqa: F401
from access_module.repository.abstract_access_repository import AbstractAccessRepository


class AccessRepository(AbstractAccessRepository):
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

    def get_user_by_email(self, email: str) -> Optional[User]:
        query = """
            SELECT 
                u.user_id, u.username, u.email, u.first_name, u.last_name, 
                u.is_active, u.is_admin, u.last_login, u.password_hash, r.rol_resource_key
            FROM Users u
            LEFT JOIN user_rols ur ON u.user_id = ur.user_id
            LEFT JOIN rols r ON ur.rol_id = r.id
            WHERE u.email = %s;
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=DictCursor
            ) as cursor:
                cursor.execute(query, (email,))
                record = cursor.fetchone()
                return self._record_to_user(record) if record else None
        except psycopg2.Error:
            return None

    def create_user(self, email: str, password: str, name: str, last_name: str) -> bool:
        query = """
            INSERT INTO Users (email, password_hash, first_name, last_name, username)
            VALUES (%s, %s, %s, %s, %s)
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (email, password, name, last_name, name))
                conn.commit()
                return True
        except psycopg2.Error:
            return False

    def change_password(self, email: str, new_password: str) -> bool:
        query = """
            UPDATE Users
            SET password_hash = %s
            WHERE email = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (new_password, email))
                conn.commit()
                return cursor.rowcount > 0
        except psycopg2.Error:
            return False
