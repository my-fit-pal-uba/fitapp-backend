from abc import abstractmethod
from routine_module.models.routine import Routine


class AbstractRoutineRepository:
    @abstractmethod
    def create_routine(self, routine: Routine) -> int:
        pass

    @abstractmethod
    def search_routine(self, name: str) -> list:
        pass

    @abstractmethod
    def filter_by_series(self, series: int) -> list:
        pass
