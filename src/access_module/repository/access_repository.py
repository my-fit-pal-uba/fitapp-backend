from typing import Optional
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore
from access_module.models.user import User
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
        )

    def get_user_by_email(self, email: str) -> Optional[User]:
        query = """
            SELECT 
                user_id, username, email, first_name, last_name, 
                is_active, is_admin, last_login, password_hash
            FROM Users
            WHERE email = %s
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
