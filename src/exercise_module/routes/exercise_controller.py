from exercise_module.services.abstract_exercise import AbstractExerciseService
from typing import Tuple
from psycopg2.errors import ForeignKeyViolation
from typing import List


class ExerciseController:
    def __init__(self, exercise_service: AbstractExerciseService):
        self.exercise_service: AbstractExerciseService = exercise_service

    def search_exercises(self, name: str) -> Tuple[bool, dict, int]:
        if not name:
            return False, {"error": "Name is required"}, 400

        exercises = self.exercise_service.search_exercises(name)
        if not exercises:
            return False, {"error": "No exercises found"}, 404

        return True, {"exercises": exercises}, 200

    def get_exercises(self) -> Tuple[bool, dict, int]:
        exercises = self.exercise_service.get_exercises()
        if not exercises:
            return False, {"error": "No exercises found"}, 404

        return True, {"exercises": exercises}, 200

    def filter_by_muscular_group(self, muscular_group: str) -> Tuple[bool, dict, int]:
        if not muscular_group:
            return False, {"error": "Muscular group is required"}, 400

        exercises = self.exercise_service.filter_by_muscular_group(muscular_group)
        if not exercises:
            return False, {"error": "No exercises found for this muscular group"}, 404

        return True, {"exercises": exercises}, 200

    def filter_by_type(self, exercise_type: str) -> Tuple[bool, dict, int]:
        if not exercise_type:
            return False, {"error": "Exercise type is required"}, 400

        exercises = self.exercise_service.filter_by_type(exercise_type)
        if not exercises:
            return False, {"error": "No exercises found for this type"}, 404

        return True, {"exercises": exercises}, 200

    def filter_by_place(self, place: str) -> Tuple[bool, dict, int]:
        if not place:
            return False, {"error": "Place is required"}, 400

        exercises = self.exercise_service.filter_by_place(place)
        if not exercises:
            return False, {"error": "No exercises found for this place"}, 404

        return True, {"exercises": exercises}, 200

    def register_series(
        self, user_id: int, exercise_id: int, series: List[dict]
    ) -> Tuple[bool, dict, int]:

        try:
            result = self.exercise_service.register_series(user_id, exercise_id, series)
            if not result:
                return False, {"error": "Failed to register series"}, 500
        except ForeignKeyViolation:
            return False, {"error": "User or Exercise not found"}, 404
        except Exception:
            return False, {"error": "Internal server error"}, 500

        return True, {"message": "Series registered successfully"}, 200

    def rate_exercise(
        self, user_id: int, exercise_id: int, rating: int
    ) -> Tuple[bool, dict, int]:
        try:
            result = self.exercise_service.rate_exercise(user_id, exercise_id, rating)
            if not result:
                return False, {"error": "Failed to rate exercise"}, 500
        except ForeignKeyViolation:
            return False, {"error": "User or Exercise not found"}, 404
        except Exception:
            return False, {"error": "Internal server error"}, 500

        return True, {"message": "Exercise rated successfully"}, 200

    def get_ratings(self, user_id: int) -> List[dict]:
        return self.exercise_service.get_ratings(user_id)

    def get_average_ratings(self) -> List[dict]:
        return self.exercise_service.get_average_ratings()

    def get_series_by_user(self, user_id: int) -> Tuple[bool, dict, int]:
        if not user_id:
            return False, {"error": "User ID is required"}, 400

        try:
            series = self.exercise_service.get_series_by_user(user_id)
            if not series:
                return False, {"error": "No series found for this user"}, 404
        except Exception as e:
            print(f"[ERROR get_series_by_user] {e}")  # <-- agregalo
            return False, {"error": "Internal server error"}, 500

        return True, {"series": series}, 200
