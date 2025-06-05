from typing import Tuple
from routine_module.services.abstract_routine_service import AbstractRoutineService

class RoutineController:
    def __init__(self, routine_service: AbstractRoutineService):
        self.routine_service: AbstractRoutineService = routine_service