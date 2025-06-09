from goals_module.services.abstract_goals_service import AbstractGoalsService
from goals_module.models.goals import Goals
from typing import List

from goals_module.repository.abstract_goals_repository import (
    AbstractGoalsRepository,
)


class GoalsService(AbstractGoalsService):
    def __init__(self, abstract_goals_service: AbstractGoalsRepository):
        self.repository: AbstractGoalsRepository = abstract_goals_service

    def save_goal(self, user_id: int, goal_value: int) -> bool:
        self.repository.save_goal(user_id, goal_value)
