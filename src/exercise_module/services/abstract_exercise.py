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
    def register_series(
        self, user_id: int, exercise_id: int, series: List[dict]
    ) -> bool:
        """Abstract method to register a series of an exercise for a user.

        :param user_id: The ID of the user.
        :param exercise_id: The ID of the exercise.
        :param repetitions: The number of repetitions in the series.
        :param weight: The weight used in the series.
        :return: A boolean indicating the success of the operation.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def rate_exercise(self, user_id: int, exercise_id: int, rating: int) -> bool:
        """Abstract method to rate an exercise by a user.

        :param user_id: The ID of the user.
        :param exercise_id: The ID of the exercise.
        :param rating: The rating given by the user.
        :return: A boolean indicating the success of the operation.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def get_ratings(self, user_id: int) -> list:
        """Abstract method to get all ratings given by a user.

        :param user_id: The ID of the user.
        :return: A list of ratings given by the user.
        """
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def get_average_ratings(self) -> list:
        """Abstract method to get average ratings for all exercises"""
        raise NotImplementedError("Subclasses should implement this method.")
