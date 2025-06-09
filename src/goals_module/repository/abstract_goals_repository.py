from abc import abstractmethod
from goals_module.models.goals import Goals
from typing import List


class AbstractGoalsRepository:
    @abstractmethod
    def save_goal(self, user_id: int, goal_value: int) -> bool:
        pass
    
    @abstractmethod
    def get_latest_goal(self, user_id: int) -> tuple:
        pass
