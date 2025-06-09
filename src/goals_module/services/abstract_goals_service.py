from abc import abstractmethod
from typing import List


class AbstractGoalsService:
    """An abstract base class that defines the interface for exercise services.
    Subclasses should implement the methods to provide concrete exercise management logic.

    Methods
    -------

    """

    @abstractmethod
    def save_goal(self, user_id: int, goal_value: int) -> bool:
        """Abstract method to save a weight goal

        :param user_id: The ID of the user.
        :param goal_value: The user goal.
        :return: A boolean indicating the success of the operation.
        """
        raise NotImplementedError("Subclasses should implement this method.")
