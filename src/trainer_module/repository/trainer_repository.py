import psycopg2  # type: ignore
from typing import Optional
from trainer_module.repository.abstract_trainer_repository import (
    AbstractTrainerRepository,
)


class TrainerRepository(AbstractTrainerRepository):
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
