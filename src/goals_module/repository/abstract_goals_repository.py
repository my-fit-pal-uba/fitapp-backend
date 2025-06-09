from abc import abstractmethod
from goals_module.models.goals import Goals


class AbstractGoalsRepository:
    @abstractmethod
    def save_goal(self, user_id: int, goal_value: int) -> bool:
        pass
