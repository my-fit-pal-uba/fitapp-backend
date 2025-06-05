from routine_module.services.abstract_routine_service import AbstractRoutineService
from routine_module.models.routine import Routine
from routine_module.repository.abstract_routine_repository import AbstractRoutineRepository

class RoutineService(AbstractRoutineService):
    def __init__(self, abstract_routine_service: AbstractRoutineRepository):
        self.repository: AbstractRoutineRepository = abstract_routine_service