from flask import Blueprint
from history_module.routes.history_controller import HistoryController
from datetime import datetime, timedelta
import random


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
              calories:
                type: number
                format: float
          400:
            description: An error occurred while processing the request.
        """

        today = datetime.now()
        history = []
        for i in range(7):
            day = today - timedelta(days=i)
            calories = round(random.uniform(1500, 3000), 2)
            history.append({"date": day.strftime("%Y-%m-%d"), "calories": calories})
        return history[::-1]
