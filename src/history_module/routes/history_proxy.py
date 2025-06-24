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
        self.history_bp.add_url_rule(
            "routine_history", view_func=self.get_routine_history, methods=["GET"]
        )
        self.history_bp.add_url_rule(
            "routine_history_by_date",
            view_func=self.get_routine_history_by_date,
            methods=["GET"],
        )
        self.history_bp.add_url_rule(
            "all_history", view_func=self.get_all_history, methods=["GET"]
        )

    def get_weight_history(self):
        """
        ---
        tags:
          - History
        summary: Retrieve user's weight consumption history
        description: Returns an array of objects containing dates and corresponding weight values
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
                    description: The date of the weight record
                  weight:
                    type: number
                    format: float
                    description: The amount of weight consumed on that date
            examples:
              application/json: [
                {"date": "2023-01-01", "weight": 2000.5},
                {"date": "2023-01-02", "weight": 1850.0}
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
            result = self.history_service.get_weight_history(user_id)
            return ResponseInfo.to_response(result)
        except Exception as e:
            return {"error": str(e)}, 400

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

    def get_routine_history(self):
        """
        ---
        tags:
          - History
        summary: Retrieve user's routine history
        description: Returns an array of objects containing dates and corresponding routine values
        parameters:
          - name: user_id
            in: query
            type: integer
            required: true
            description: The ID of the user whose routine history is being requested
        responses:
          200:
            description: Routine history retrieved successfully
            schema:
              type: array
              items:
                type: object
                properties:
                  date:
                    type: string
                    format: date
                    description: The date of the routine record
                  routine:
                    type: string
                    description: The routine performed on that date
            examples:
              application/json: [
                {"date": "2023-01-01", "routine": "Morning Run"},
                {"date": "2023-01-02", "routine": "Evening Yoga"}
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
        data = request.args.to_dict()
        user_id = data.get("user_id", None)
        if not user_id:
            return ResponseInfo.to_response((False, "User_id is required", 400))
        result = self.history_service.get_routine_history(user_id)
        return ResponseInfo.to_response((True, result, 200))

    def get_routine_history_by_date(self):
        """
        ---
        tags:
          - History
        summary: Retrieve user's routine history by date
        description: Returns an array of objects containing dates and corresponding routine values for a specific date
        parameters:
          - name: user_id
            in: query
            type: integer
            required: true
            description: The ID of the user whose routine history is being requested
          - name: date
            in: query
            type: string
            required: true
            description: "The date for which the routine history is being requested (format: YYYY-MM-DD)"
        responses:
          200:
            description: Routine history retrieved successfully
            schema:
              type: array
              items:
                type: object
                properties:
                  date:
                    type: string
                    format: date
                    description: The date of the routine record
                  routine:
                    type: string
                    description: The routine performed on that date
            examples:
              application/json: [
                {"date": "2023-01-01", "routine": "Morning Run"},
                {"date": "2023-01-02", "routine": "Evening Yoga"}
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
        data = request.args.to_dict()
        user_id = data.get("user_id", None)
        date = data.get("date", None)
        if not user_id or not date:
            return ResponseInfo.to_response(
                (False, "User_id and date are required", 400)
            )

        result = self.history_service.get_routine_history_by_date(user_id, date)
        return ResponseInfo.to_response((True, result, 200))

    def get_all_history(self):
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
            result = self.history_service.get_all_history(user_id)
            return ResponseInfo.to_response(result)
        except Exception as e:
            return {"error": str(e)}, 400
