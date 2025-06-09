from goals_module.services.abstract_goals_service import AbstractGoalsService
from typing import Tuple
from typing import List


class GoalsController:

    def __init__(self, goals_service: AbstractGoalsService):
        self.goals_service: AbstractGoalsService = goals_service

    def save_goal(self, user_id: int, goal_value: int):
        try:
            self.goals_service.save_goal(user_id, goal_value)
            return [], "Success", 200
        except Exception:
            return [], "An error has ocurred", 500

    def get_latest_goal(self, user_id: int) -> Tuple[bool, dict, int]:
        try:
            goal = self.goals_service.get_latest_goal(user_id)
            return goal
        except Exception:
            return False, "An error has ocurred", 500
        
    def get_goal_history(self, user_id: int) -> Tuple[bool, dict, int]:
        try:
            return self.goals_service.get_all_goals_by_user(user_id)
        except Exception as e:
            print(f"Error en get_goal_history: {e}")
            return False, "An error has occurred: " + str(e), 500
