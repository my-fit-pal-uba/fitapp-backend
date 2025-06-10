from routine_module.models.routine import Routine
from exercise_module.models.exercise import Exercise
import psycopg2  # type: ignore
from typing import Optional
from routine_module.repository.abstract_routine_repository import (
    AbstractRoutineRepository,
)


class RoutineRepository(AbstractRoutineRepository):
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

    def _record_to_routine(self, record) -> Routine:
        return Routine(
            routine_id=record["routine_id"],
            name=record["name"],
            description=record["description"],
            series=record["series"],
            muscular_group=record["muscular_group"],
        )

    def _record_to_exercise(self, record) -> Exercise:
        return Exercise(
            exercise_id=record["exercise_id"],
            name=record["name"],
            description=record["description"],
            muscular_group=record["muscular_group"],
            type=record["type"],
            place=record["place"],
            photo_guide=record.get("photo_guide"),
            video_guide=record.get("video_guide"),
        )

    def create_routine(self, routine: Routine) -> int:
        insert_routine_query = """
        INSERT INTO Routines (name, muscular_group, description, series)
        VALUES (%s, %s, %s, %s)
        RETURNING routine_id
        """
        insert_relation_query = """
            INSERT INTO Routine_Exercises (routine_id, exercise_id)
            VALUES (%s, %s)
        """

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        insert_routine_query,
                        (
                            routine.name,
                            routine.muscular_group,
                            routine.description,
                            routine.series,
                        ),
                    )
                    routine_id = cursor.fetchone()[0]

                    for exercise in routine.exercises:
                        cursor.execute(
                            insert_relation_query, (routine_id, exercise.exercise_id)
                        )

                conn.commit()
                return routine_id

        except psycopg2.Error as e:
            print("Error al guardar la rutina:", e)
            return None

    def search_routine(self, name: str) -> list:
        routine_query = """
            SELECT routine_id, name, muscular_group, description, series
            FROM Routines
            WHERE name ILIKE %s
        """

        exercises_query = """
            SELECT e.exercise_id, e.name, e.description, e.muscular_group, e.type, e.place,
                e.photo_guide, e.video_guide
            FROM Exercises e
            JOIN Routine_Exercises re ON e.exercise_id = re.exercise_id
            WHERE re.routine_id = %s
        """

        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(routine_query, (f"%{name}%",))
                routines_data = cursor.fetchall()

                routines = []
                for row in routines_data:
                    routine_id = row["routine_id"]

                    cursor.execute(exercises_query, (routine_id,))
                    exercises_data = cursor.fetchall()
                    exercises = [self._record_to_exercise(e) for e in exercises_data]

                    routine = Routine(
                        routine_id=routine_id,
                        name=row["name"],
                        muscular_group=row["muscular_group"],
                        description=row["description"],
                        series=row["series"],
                        exercises=exercises,
                    )
                    routines.append(routine)

                return routines

        except psycopg2.Error as e:
            print("Error al buscar rutina:", e)
            return []

    def filter_by_series(self, series: int) -> list:
        routine_query = """
            SELECT routine_id, name, muscular_group, description, series
            FROM Routines
            WHERE series = %s
        """

        exercises_query = """
            SELECT e.exercise_id, e.name, e.description, e.muscular_group, e.type, e.place,
                e.photo_guide, e.video_guide
            FROM Exercises e
            JOIN Routine_Exercises re ON e.exercise_id = re.exercise_id
            WHERE re.routine_id = %s
        """

        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(routine_query, (series,))
                routines_data = cursor.fetchall()

                routines = []
                for row in routines_data:
                    routine_id = row["routine_id"]

                    # Obtener ejercicios asociados a la rutina
                    cursor.execute(exercises_query, (routine_id,))
                    exercises_data = cursor.fetchall()
                    exercises = [self._record_to_exercise(e) for e in exercises_data]

                    routine = Routine(
                        routine_id=routine_id,
                        name=row["name"],
                        muscular_group=row["muscular_group"],
                        description=row["description"],
                        series=row["series"],
                        exercises=exercises,
                    )
                    routines.append(routine)

                return routines

        except psycopg2.Error as e:
            print("Error al filtrar por series:", e)
            return []

    def get_all_routines(self) -> list:
        routine_query = """
            SELECT routine_id, name, muscular_group, description, series
            FROM Routines
        """

        exercises_query = """
            SELECT e.exercise_id, e.name, e.description, e.muscular_group, e.type, e.place,
                e.photo_guide, e.video_guide
            FROM Exercises e
            JOIN Routine_Exercises re ON e.exercise_id = re.exercise_id
            WHERE re.routine_id = %s
        """

        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(
                    routine_query,
                )
                routines_data = cursor.fetchall()

                routines = []
                for row in routines_data:
                    routine_id = row["routine_id"]

                    cursor.execute(exercises_query, (routine_id,))
                    exercises_data = cursor.fetchall()
                    exercises = [self._record_to_exercise(e) for e in exercises_data]

                    routine = Routine(
                        routine_id=routine_id,
                        name=row["name"],
                        muscular_group=row["muscular_group"],
                        description=row["description"],
                        series=row["series"],
                        exercises=exercises,
                    )
                    routines.append(routine)

                return routines

        except psycopg2.Error as e:
            print("Error al buscar rutina:", e)
            return []

    def rate_routine(self, user_id: int, routine_id: int, rating: int) -> bool:
        query = """
            INSERT INTO routine_ratings (user_id, routine_id, rating)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, routine_id) DO UPDATE SET rating = EXCLUDED.rating
        """
        with self.get_connection() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(query, (user_id, routine_id, rating))
            conn.commit()
            return True

    def get_ratings(self, user_id: int) -> list:
        query = """
            SELECT routine_id, rating
            FROM routine_ratings
            WHERE user_id = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (user_id,))
                records = cursor.fetchall()
                return [
                    {
                        "routine_id": record["routine_id"],
                        "rating": float(record["rating"]),
                    }
                    for record in records
                ]
        except psycopg2.Error:
            return []

    def get_average_ratings(self) -> list:
        query = """
            SELECT e.routine_id AS routine_id, COALESCE(AVG(r.rating), 0) AS average_rating
            FROM routines e
            LEFT JOIN routine_ratings r ON e.routine_id = r.routine_id
            GROUP BY e.routine_id
            ORDER BY e.routine_id
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
                return [
                    {
                        "routine_id": record["routine_id"],
                        "average_rating": float(record["average_rating"]),
                    }
                    for record in records
                ]
        except psycopg2.Error:
            return []

    def register(self, user_id: int, routine_id: int) -> bool:
        query = """
            INSERT INTO done_routines (user_id, routine_id)
            VALUES (%s, %s);
        """

        with self.get_connection() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(query, (user_id, routine_id))
            conn.commit()
            return True

    def get_routine_by_id(self, routine_id: int) -> Optional[dict]:
        query = """
            SELECT * FROM routines WHERE routine_id = %s
        """
        exercises_query = """
            SELECT e.*
            FROM exercises e
            JOIN routine_exercises re ON e.exercise_id = re.exercise_id
            WHERE re.routine_id = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (routine_id,))
                routine_record = cursor.fetchone()
                if not routine_record:
                    return None
                cursor.execute(exercises_query, (routine_id,))
                exercises = cursor.fetchall()
                return {
                    "routine_id": routine_record["routine_id"],
                    "name": routine_record["name"],
                    "description": routine_record["description"],
                    "muscular_group": routine_record["muscular_group"],
                    "series": routine_record["series"],
                    "exercises": [
                        {
                            "exercise_id": ex["exercise_id"],
                            "name": ex["name"],
                            "description": ex["description"],
                            "muscular_group": ex["muscular_group"],
                            "type": ex["type"],
                            "place": ex["place"],
                            "photo_guide": ex.get("photo_guide"),
                            "video_guide": ex.get("video_guide"),
                        }
                        for ex in exercises
                    ],
                }
        except psycopg2.Error:
            return None
