from flask import Blueprint, request
from goals_module.routes.goals_controller import GoalsController

from models.response import ResponseInfo


class GoalsProxy:
    def __init__(self, goals_controller: GoalsController):
        self.goals_controller: GoalsController = goals_controller
        self.goals_bp = Blueprint("goals", __name__, url_prefix="/goals")
        self.register_routes()

    def register_routes(self):
        self.goals_bp.add_url_rule(
            "/register", view_func=self.save_goal, methods=["POST"]
        )

    def save_goal(self):
        """
        Guarda un objetivo de peso para un usuario
        ---
        tags:
          - Goals
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - user_id
                - goal_value
              properties:
                user_id:
                  type: integer
                  example: 12
                goal_value:
                  type: number
                  format: float
                  example: 72.5
        responses:
          200:
            description: Objetivo guardado exitosamente
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
          400:
            description: Datos inválidos
          404:
            description: Usuario no encontrado
          500:
            description: Error del servidor
        """
        data = request.get_json()
        user_id = data.get("user_id")
        goal_value = data.get("goal_value")

        if not user_id or goal_value is None:
            return ResponseInfo.to_response(
                (False, "Se requieren 'user_id' y 'goal_value'", 400)
            )

        self.goals_controller.save_goal(user_id, goal_value)

        return ResponseInfo.to_response((True, "Objetivo guardado", 200))
