from exercise_module.services.abstract_exercise import AbstractExerciseService
from exercise_module.models.exercise import Exercise
from exercise_module.models.serie import Serie
from typing import List

from exercise_module.repository.abstract_exercise_repository import (
    AbstractExerciseRepository,
)


class ExerciseService(AbstractExerciseService):
    def __init__(self, abstract_exercise_service: AbstractExerciseRepository):
        self.repository: AbstractExerciseRepository = abstract_exercise_service

    def search_exercises(self, name: str) -> list:
        if not name:
            return []

        exercises = self.repository.search_exercises(name)
        if not exercises:
            return []

        return [exercise.to_dict() for exercise in exercises]

    def get_exercises(self) -> list:
        exercises = self.repository.get_exercises()
        if not exercises:
            return []

        return [exercise.to_dict() for exercise in exercises]

    def filter_by_muscular_group(self, muscular_group: str) -> list:
        if not muscular_group:
            return []

        exercises = self.repository.filter_by_muscular_group(muscular_group)
        if not exercises:
            return []

        return [exercise.to_dict() for exercise in exercises]

    def filter_by_place(self, place: str) -> list:
        if not place:
            return []

        exercises = self.repository.filter_by_place(place)
        if not exercises:
            return []

        return [exercise.to_dict() for exercise in exercises]

    def filter_by_type(self, type: str) -> list:
        if not type:
            return []

        exercises = self.repository.filter_by_type(type)
        if not exercises:
            return []

        return [exercise.to_dict() for exercise in exercises]

    def register_series(
        self, user_id: int, exercise_id: int, series: List[dict]
    ) -> bool:

        for serie in series:
            repetitions = serie.get("repetitions")
            weight = serie.get("weight")

            result = self.repository.register_serie(
                Serie(
                    user_id=user_id,
                    exercise_id=exercise_id,
                    repetitions=repetitions,
                    weight=weight,
                )
            )

            if not result:
                return False

        return True

    def rate_exercise(
        self, user_id: int, exercise_id: int, rating: int
    ) -> bool:
        if not user_id or not exercise_id or not rating:
            return False

        result = self.repository.rate_exercise(user_id, exercise_id, rating)
        return result