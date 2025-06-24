import psycopg2  # type: ignore
from typing import Optional
from trainer_module.repository.abstract_trainer_repository import (
    AbstractTrainerRepository,
)
import os
from urllib.parse import urlparse

class TrainerRepository(AbstractTrainerRepository):
    def __init__(self, db_config=None):
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            result = urlparse(database_url)
            self.db_config = {
                "host": result.hostname,
                "database": result.path.lstrip('/'),
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

    def find_patient_by_full_identity(
        self, nombre: str, apellido: str, patient_id: int
    ):
        query = """
            SELECT * FROM users
            WHERE first_name = %s AND last_name = %s AND user_id = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (nombre, apellido, patient_id))
                return cursor.fetchone()
        except psycopg2.Error as e:
            print("Error buscando usuario:", e)
            return None

    def link_patient_to_trainer(self, patient_id: int, trainer_id: int) -> None:
        check_query = """
            SELECT trainer_id FROM trainer_client WHERE client_id = %s
        """
        insert_query = """
            INSERT INTO trainer_client (trainer_id, client_id) VALUES (%s, %s)
        """
        update_query = """
            UPDATE trainer_client SET trainer_id = %s WHERE client_id = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(check_query, (patient_id,))
                record = cursor.fetchone()

                if record:
                    existing_trainer_id = record[0]
                    if existing_trainer_id == trainer_id:
                        raise ValueError("Ya tienes a este cliente registrado")
                    else:
                        cursor.execute(update_query, (trainer_id, patient_id))
                else:
                    cursor.execute(insert_query, (trainer_id, patient_id))

                conn.commit()
        except psycopg2.Error as e:
            print("Error vinculando paciente a entrenador:", e)
            raise

    def get_clients_by_trainer(self, trainer_id: int) -> list[dict]:
        query = """
            SELECT u.user_id, u.first_name, u.last_name
            FROM trainer_client tc
            JOIN users u ON tc.client_id = u.user_id
            WHERE tc.trainer_id = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (trainer_id,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except psycopg2.Error as e:
            print("Error al obtener clientes del entrenador:", e)
            return []

    def exercise_exists(self, exercise_id: int) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM exercises WHERE exercise_id = %s)"
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (exercise_id,))
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            print("Error verificando existencia de ejercicio:", e)
            return False

    def client_exists(self, client_id: int) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s)"
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (client_id,))
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            print("Error verificando existencia de cliente:", e)
            return False

    def share_exercise(self, exercise_id: int, client_id: int) -> None:
        query = """
            INSERT INTO client_exercises (client_id, exercise_id)
            VALUES (%s, %s)
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (client_id, exercise_id))
                conn.commit()
        except psycopg2.Error as e:
            print("Error compartiendo ejercicio:", e)
            raise

    def dish_exists(self, dish_id: int) -> bool:
        query = "SELECT EXISTS(SELECT 1 FROM dishes WHERE id = %s)"
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (dish_id,))
                return cursor.fetchone()[0]
        except psycopg2.Error as e:
            print("Error verificando existencia de plato:", e)
            return False

    def share_dish(self, dish_id: int, client_id: int) -> None:
        query = """
            INSERT INTO client_dishes (client_id, dish_id)
            VALUES (%s, %s)
        """
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (client_id, dish_id))
                conn.commit()
        except psycopg2.Error as e:
            print("Error compartiendo plato:", e)
            raise

    def client_dishes(self, client_id: int) -> list[dict]:
        query = "SELECT dish_id FROM client_dishes WHERE client_id = %s"
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (client_id,))
                dish_ids = [row[0] for row in cursor.fetchall()]
            return [self.get_dish_by_id(dish_id) for dish_id in dish_ids]
        except psycopg2.Error as e:
            print("Error obteniendo platos del cliente:", e)
            return []

    def client_exercises(self, client_id: int) -> list[dict]:
        query = "SELECT exercise_id FROM client_exercises WHERE client_id = %s"
        try:
            with self.get_connection() as conn, conn.cursor() as cursor:
                cursor.execute(query, (client_id,))
                exercise_ids = [row[0] for row in cursor.fetchall()]
            return [self.get_exercise_by_id(ex_id) for ex_id in exercise_ids]
        except psycopg2.Error as e:
            print("Error obteniendo ejercicios del cliente:", e)
            return []

    def get_dish_by_id(self, dish_id: int) -> Optional[dict]:
        query = "SELECT * FROM dishes WHERE id = %s"
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (dish_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except psycopg2.Error as e:
            print("Error obteniendo plato:", e)
            return None

    def get_exercise_by_id(self, exercise_id: int) -> Optional[dict]:
        query = "SELECT * FROM exercises WHERE exercise_id = %s"
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (exercise_id,))
                row = cursor.fetchone()
                return dict(row) if row else None
        except psycopg2.Error as e:
            print("Error obteniendo ejercicio:", e)
            return None
