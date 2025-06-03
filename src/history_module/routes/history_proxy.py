from flask import Blueprint, request
from history_module.routes.history_controller import HistoryController

from models.response import ResponseInfo


class HistoryProxy:
    def __init__(self, history_controller: HistoryController):
        self.history_service: HistoryController = history_controller
        self.history_bp = Blueprint("history", __name__, url_prefix="/history")
        self.register_routes()

    def register_routes(self):
        self.history_bp.add_url_rule(
            "/weight_history", view_func=self.get_weight_history, methods=["GET"]
        )
        self.history_bp.add_url_rule(
            "/calories_history", view_func=self.get_calories_history, methods=["GET"]
        )

    def get_weight_history(self):
        pass

    def get_calories_history(self):
        """
        ---
        tags:
          - History
        summary: Retrieve user's calories consumption history
        description: Returns an array of objects containing dates and corresponding calories values
        parameters:
          - name: user_id
            in: query
            type: integer
            required: true
            description: The ID of the user whose calories history is being requested
        responses:
          200:
            description: Calories history retrieved successfully
            schema:
              type: array
              items:
                type: object
                properties:
                  date:
                    type: string
                    format: date
                    description: The date of the calories record
                  calories:
                    type: number
                    format: float
                    description: The amount of calories consumed on that date
            examples:
              application/json: [
                {"date": "2023-01-01", "calories": 2000.5},
                {"date": "2023-01-02", "calories": 1850.0}
              ]
          400:
            description: An error occurred while processing the request
            schema:
              type: object
              properties:
                error:
                  type: string
                  description: Error message
        """
        try:
            data = request.args.to_dict()
            user_id = data.get("user_id", None)
            if not user_id:
                return {"error": "User ID is required"}, 400
            result = self.history_service.get_calories_history(user_id)
            return ResponseInfo.to_response(result)
        except Exception as e:
            return {"error": str(e)}, 400
