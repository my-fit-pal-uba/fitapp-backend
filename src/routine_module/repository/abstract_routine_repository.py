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

    @abstractmethod
    def get_all_routines(self) -> list:
        pass

    @abstractmethod
    def rate_routine(self, user_id: int, routine_id: int, rating: int) -> bool:
        """
        Rate an routine by a user.

        :param user_id: The ID of the user.
        :param routine_id: The ID of the routine.
        :param rating: The rating given by the user.
        :return: A boolean indicating the success of the operation.
        """
        pass

    @abstractmethod
    def get_ratings(self, user_id: int) -> list:
        """
        Get all ratings given by a user.

        :param user_id: The ID of the user.
        :return: A list of ratings given by the user.
        """
        pass

    @abstractmethod
    def get_average_ratings(self) -> list:
        """
        Get average ratings for all routines.

        :return: A list of dictionaries containing routine IDs and their average ratings.
        """
        pass

    @abstractmethod
    def register(self, user_id: int, routine_id: int) -> bool:
        """
        Register that the user realized a routine

        :param user_id: The ID of the user.
        :param routine_id: The ID of the routine.
        """
        pass