from abc import abstractmethod
from typing import List


class AbstractExerciseService:
    """An abstract base class that defines the interface for exercise services.
    Subclasses should implement the methods to provide concrete exercise management logic.

    Methods
    -------
    search_exercises(name: str) -> list
        Abstract method for searching exercises by name.
        Should return a list of exercises matching the name.

    get_exercises() -> list
        Abstract method for retrieving all exercises.
        Should return a list of all available exercises.

    filter_by_muscular_group(self, muscular_group: str) -> list:
        Abstract method to filter exercises by muscular group.
        Should return a list of all available exercises.

    filter_by_place(self, place: str) -> list:
        Abstract method to filter exercises by place.
        Should return a list of all available exercises.

    filter_by_type(self, type: str) -> list:
        Abstract method to filter exercises by type.
        Should return a list of all available exercises.
    """

    @abstractmethod
    def search_exercises(self, name: str) -> list:
        """Abstract method to search exercises by name."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def get_exercises(self) -> list:
        """Abstract method to retrieve all exercises."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def filter_by_muscular_group(self, muscular_group: str) -> list:
        """Abstract method to filter exercises by muscular group."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def filter_by_place(self, place: str) -> list:
        """Abstract method to filter exercises by place."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def filter_by_type(self, type: str) -> list:
        """Abstract method to filter exercises by type."""
        raise NotImplementedError("Subclasses should implement this method.")
    
    @abstractmethod
    def register_series(self, user_id: int, exercise_id: int, series: List[dict]) -> bool:
        """Abstract method to register a series of an exercise for a user.
        
        :param user_id: The ID of the user.
        :param exercise_id: The ID of the exercise.
        :param repetitions: The number of repetitions in the series.
        :param weight: The weight used in the series.
        :return: A boolean indicating the success of the operation.
        """
        raise NotImplementedError("Subclasses should implement this method.")
