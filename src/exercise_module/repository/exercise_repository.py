from exercise_module.models.exercise import Exercise
from exercise_module.models.serie import Serie
import psycopg2  # type: ignore
from exercise_module.repository.abstract_exercise_repository import (
    AbstractExerciseRepository,
)


class ExerciseRepository(AbstractExerciseRepository):
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

    def search_exercises(self, name: str) -> list:
        query = """
            SELECT 
                exercise_id, name, description, muscular_group, type, place, 
                photo_guide, video_guide
            FROM Exercises
            WHERE name ILIKE %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (name,))
                records = cursor.fetchall()
                return [self._record_to_exercise(record) for record in records]
        except psycopg2.Error:
            return []

    def get_exercises(self) -> list:
        query = """
            SELECT 
                exercise_id, name, description, muscular_group, type, place, 
                photo_guide, video_guide
            FROM Exercises
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
                return [self._record_to_exercise(record) for record in records]
        except psycopg2.Error:
            return []

    def filter_by_muscular_group(self, muscular_group: str) -> list:
        query = """
            SELECT 
                exercise_id, name, description, muscular_group, type, place, 
                photo_guide, video_guide
            FROM Exercises
            WHERE muscular_group = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (muscular_group,))
                records = cursor.fetchall()
                return [self._record_to_exercise(record) for record in records]
        except psycopg2.Error:
            return []

    def filter_by_type(self, type_: str) -> list:
        query = """
            SELECT 
                exercise_id, name, description, muscular_group, type, place, 
                photo_guide, video_guide
            FROM Exercises
            WHERE type = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (type_,))
                records = cursor.fetchall()
                return [self._record_to_exercise(record) for record in records]
        except psycopg2.Error:
            return []

    def filter_by_place(self, place: str) -> list:
        query = """
            SELECT 
                exercise_id, name, description, muscular_group, type, place, 
                photo_guide, video_guide
            FROM Exercises
            WHERE place = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (place,))
                records = cursor.fetchall()
                return [self._record_to_exercise(record) for record in records]
        except psycopg2.Error:
            return []


    def get_by_id(self, exercise_id: int) -> Exercise:
        query = """
            SELECT 
                exercise_id, name, description, muscular_group, type, place, 
                photo_guide, video_guide
            FROM Exercises
            WHERE exercise_id = %s
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query, (exercise_id,))
                record = cursor.fetchone()
                return self._record_to_exercise(record) if record else None
        except psycopg2.Error:
            return None

    def register_serie(self, serie: Serie) -> bool:
        query = """
            INSERT INTO series (user_id, exercise_id, reps, weight)
            VALUES (%s, %s, %s, %s)
        """
        with self.get_connection() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(
                query,
                (serie.user_id, serie.exercise_id, serie.repetitions, serie.weight),
            )
            conn.commit()
            return True

    def rate_exercise(self, user_id: int, exercise_id: int, rating: int) -> bool:
        query = """
            INSERT INTO exercise_ratings (user_id, exercise_id, rating)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, exercise_id) DO UPDATE SET rating = EXCLUDED.rating
        """
        with self.get_connection() as conn, conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as cursor:
            cursor.execute(query, (user_id, exercise_id, rating))
            conn.commit()
            return True

    def get_ratings(self, user_id: int) -> list:
        query = """
            SELECT exercise_id, rating
            FROM exercise_ratings
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
                        "exercise_id": record["exercise_id"],
                        "rating": float(record["rating"]),
                    }
                    for record in records
                ]
        except psycopg2.Error:
            return []

    def get_average_ratings(self) -> list:
        query = """
            SELECT e.exercise_id AS exercise_id, COALESCE(AVG(r.rating), 0) AS average_rating
            FROM exercises e
            LEFT JOIN exercise_ratings r ON e.exercise_id = r.exercise_id
            GROUP BY e.exercise_id
            ORDER BY e.exercise_id
        """
        try:
            with self.get_connection() as conn, conn.cursor(
                cursor_factory=psycopg2.extras.DictCursor
            ) as cursor:
                cursor.execute(query)
                records = cursor.fetchall()
                return [
                    {
                        "exercise_id": record["exercise_id"],
                        "average_rating": float(record["average_rating"]),
                    }
                    for record in records
                ]
        except psycopg2.Error:
            return []
