from typing import List
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2 import sql
from src.models.user import User

# Configuración de la conexión (usa las variables de tu docker-compose.yml)
DB_CONFIG = {
    "host": "db",  # o "db" si estás dentro de Docker
    "database": "app_db",
    "user": "app_user",
    "password": "app_password",
    "port": "5432",
}


def get_connection():
    """Establece conexión con la base de datos."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None


def get_users() -> List[User]:
    """
    Retrieve all users from the database and map them to User objects.

    Returns:
        List[User]: A list of User objects sorted by user_id

    Raises:
        DatabaseError: If there's any database connectivity issue
        DataError: If there's an issue with the data format
    """
    query = sql.SQL(
        """
        SELECT 
            user_id, 
            username, 
            email, 
            first_name, 
            last_name, 
            is_active, 
            is_admin, 
            last_login 
        FROM {} 
    """
    ).format(
        sql.Identifier("users")
    )  # Safe table name quoting

    conn = None
    try:
        conn = get_connection()
        if conn is None:
            raise psycopg2.DatabaseError("Database connection failed")

        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(query)

            if cursor.rowcount == 0:
                return []

            users = []
            for record in cursor:
                try:
                    users.append(
                        User(
                            user_id=record["user_id"],
                            username=record["username"],
                            email=record["email"],
                            first_name=record["first_name"],
                            last_name=record["last_name"],
                            is_active=record["is_active"],
                            is_superuser=record["is_admin"],
                            last_login=(
                                record["last_login"] if record["last_login"] else None
                            ),
                        )
                    )
                except (KeyError, TypeError) as e:
                    raise psycopg2.DataError(
                        f"Data format error in record {record}: {e}"
                    )

            return users

    except psycopg2.Error as e:
        # Log the error here (consider using logging module)
        raise psycopg2.DatabaseError(f"Database operation failed: {e}")
    finally:
        if conn:
            conn.close()
