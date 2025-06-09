from goals_module.services.abstract_goals_service import AbstractGoalsService


class GoalsController:

    def __init__(self, goals_service: AbstractGoalsService):
        self.goals_service: AbstractGoalsService = goals_service

    def save_goal(self, user_id: int, goal_value: int):
        try:
            calories_history = self.goals_service.save_goal(user_id, goal_value)
            return calories_history, "Success", 200
        except Exception:
            return [], "An error has ocurred", 500
