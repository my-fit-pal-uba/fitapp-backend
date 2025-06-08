from abc import abstractmethod
from typing import List


class AbstractRoutineService:
    """An abstract base class that defines the interface for routine services.
    Subclasses should implement the methods to provide concrete routine management logic.

    Methods
    -------
    create_routine(self, data: dict) -> dict:
        Abstract method to create routines.
        Should return a dictionary representing the created routine.

    search_routines(self, name: str) -> list:
        Abstract method to search routines by name.
        Should return a list of routines matching the name.

    filter_by_series(self, series: int) -> list:
        Abstract method to filter routines by series.
        Should return a list of routines that match the specified series.

    get_all_routines(self, name: str) -> list:
        Abstract method to get all routines
        Should return a list of all routines.
    """

    @abstractmethod
    def create_routine(self, data: dict) -> dict:
        """Abstract method to create routines."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def search_routines(self, name: str) -> list:
        """Abstract method to search routines by name."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def filter_by_series(self, series: int) -> list:
        """Abstract method to filter routines by series."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def get_all_routines(self, name: str) -> list:
        """Abstract method to get all routines."""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def rate_routine(self, user_id: int, routine_id: int, rating: int) -> bool:
        """Abstract method to rate an routine by a user.

        :param user_id: The ID of the user.
        :param routine_id: The ID of the routine.
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
        """Abstract method to get average ratings for all routines"""
        raise NotImplementedError("Subclasses should implement this method.")

    @abstractmethod
    def register(self, user_id: int, routine_id: int) -> bool:
        """Abstract method to register a series of an routine for a user.

        :param user_id: The ID of the user.
        :param routine_id: The ID of the routine.
        :return: A boolean indicating the success of the operation.
        """
        raise NotImplementedError("Subclasses should implement this method.")
