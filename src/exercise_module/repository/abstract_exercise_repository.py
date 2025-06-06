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
    
    @abstractmethod
    def rate_exercise(self, user_id: int, exercise_id: int, rating: int) -> bool:
        """
        Rate an exercise by a user.

        :param user_id: The ID of the user.
        :param exercise_id: The ID of the exercise.
        :param rating: The rating given by the user.
        :return: A boolean indicating the success of the operation.
        """
        pass
    
    def get_ratings(self, user_id: int) -> list:
        """
        Get all ratings given by a user.

        :param user_id: The ID of the user.
        :return: A list of ratings given by the user.
        """
        pass
