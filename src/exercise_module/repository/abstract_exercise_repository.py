from abc import abstractmethod
from exercise_module.models.serie import Serie


class AbstractExerciseRepository:
    @abstractmethod
    def search_exercises(self, name: str) -> list:
        pass

    @abstractmethod
    def get_exercises(self) -> list:
        pass

    @abstractmethod
    def filter_by_muscular_group(self, muscular_group: str) -> list:
        pass

    @abstractmethod
    def filter_by_type(self, type: str) -> list:
        pass

    @abstractmethod
    def filter_by_place(self, place: str) -> list:
        pass

    @abstractmethod
    def register_serie(self, serie: Serie) -> bool:
        """
        Register a serie of an exercise for an user.

        :param serie: The Serie object containing the details of the exercise series.
        """
        pass
