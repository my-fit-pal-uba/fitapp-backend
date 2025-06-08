from routine_module.services.abstract_routine_service import AbstractRoutineService
from routine_module.models.routine import Routine
from routine_module.repository.abstract_routine_repository import (
    AbstractRoutineRepository,
)

from typing import List
from exercise_module.repository.exercise_repository import ExerciseRepository


class RoutineService(AbstractRoutineService):
    def __init__(self, abstract_routine_service: AbstractRoutineRepository):
        self.repository: AbstractRoutineRepository = abstract_routine_service
        self.exercise_repository = ExerciseRepository()

    def create_routine(self, data: dict) -> dict:
        if not data:
            return {}

        exercises = []
        for ex in data["exercises"]:
            # ex puede ser un dict {"exercise_id": 42} o un int
            if isinstance(ex, dict):
                ex_id = ex.get("exercise_id")
            else:
                ex_id = ex
            exercise = self.exercise_repository.get_by_id(ex_id)
            if exercise:
                exercises.append(exercise)
        routine = Routine(
            name=data["name"],
            muscular_group=data["muscular_group"],
            description=data["description"],
            series=data["series"],
            exercises=exercises,
        )
        routine_id = self.repository.create_routine(routine)
        if not routine_id:
            return {}
        routine.routine_id = routine_id
        return routine.to_dict()

    def search_routines(self, name: str) -> list:
        if not name:
            return []

        routines = self.repository.search_routine(name)
        if not routines:
            return []

        return [routine.to_dict() for routine in routines]

    def filter_by_series(self, series: int) -> list:
        if not series:
            return []

        routines = self.repository.filter_by_series(series)
        if not routines:
            return []

        return [routine.to_dict() for routine in routines]

    def get_all_routines(self) -> list:
        routines = self.repository.get_all_routines()

        if not routines:
            return []

        return [routine.to_dict() for routine in routines]
    
    def rate_routine(self, user_id: int, routine_id: int, rating: int) -> bool:
        if not user_id or not routine_id or not rating:
            return False

        result = self.repository.rate_routine(user_id, routine_id, rating)
        return result

    def get_ratings(self, user_id: int) -> List[dict]:
        return self.repository.get_ratings(user_id)

    def get_average_ratings(self) -> List[dict]:
        return self.repository.get_average_ratings()

    def register(
        self, user_id: int, routine_id: int
    ) -> bool:
        return self.repository.register(user_id, routine_id)