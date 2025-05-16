import psycopg2
from psycopg2 import sql

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


def get_users():
    """Obtiene todos los usuarios de la tabla Users."""
    query = "SELECT * FROM Users;"
    try:
        conn = get_connection()
        if not conn:
            return ["Vacio"]
        print("Pase por aca")
        with conn.cursor() as cursor:
            cursor.execute(query)
            users = cursor.fetchall()
        return users
    except psycopg2.Error as e:
        print(f"Error al obtener usuarios: {e}")
        return []
    finally:
        if conn:
            conn.close()
