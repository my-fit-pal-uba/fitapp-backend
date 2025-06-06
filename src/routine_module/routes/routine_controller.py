from typing import Tuple
from routine_module.services.abstract_routine_service import AbstractRoutineService


class RoutineController:
    def __init__(self, routine_service: AbstractRoutineService):
        self.routine_service: AbstractRoutineService = routine_service

    def create_routine(self, data: dict) -> Tuple[bool, dict, int]:
        if not data or not data.get("name"):
            return False, {"error": "Name is required"}, 400

        routine = self.routine_service.create_routine(data)
        if not routine:
            return False, {"error": "Failed to create routine"}, 500

        return True, {"routine": routine}, 200

    def search_routine(self, name: str) -> Tuple[bool, dict, int]:
        if not name:
            return False, {"error": "Name is required"}, 400

        routines = self.routine_service.search_routines(name)
        if not routines:
            return False, {"error": "No routines found"}, 404

        return True, {"routines": routines}, 200

    def filter_by_series(self, series: str) -> Tuple[bool, dict, int]:
        if not series:
            return False, {"error": "Series is required"}, 400

        routines = self.routine_service.filter_by_series(series)
        if not routines:
            return False, {"error": "No routines found"}, 404

        return True, {"routines": routines}, 200

    def get_all_routines(self) -> Tuple[bool, dict, int]:
        routines = self.routine_service.get_all_routines()
        if not routines:
            return False, {"error": "No routines found"}, 404

        return True, {"routines": routines}, 200
