from flask import Blueprint, request

from routine_module.routes.routine_controller import RoutineController
from models.response import ResponseInfo


class RoutineProxy:
    def __init__(self, routine_controller: RoutineController):
        self.routine_controller = routine_controller
        self.routine_bp = Blueprint("routine", __name__, url_prefix="/routines")
        self.register_routes()

    def register_routes(self):
        self.routine_bp.add_url_rule("/create", view_func=self.create, methods=["POST"])
        self.routine_bp.add_url_rule("/search", view_func=self.search, methods=["GET"])
        self.routine_bp.add_url_rule(
            "/filter_by_series", view_func=self.filter_by_series, methods=["GET"]
        )

    def create(self):
        """
        Crea una rutina
        ---
        tags:
          - Routine
        parameters:
          - in: body
            name: routine
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: Full Body Workout
                muscular_group:
                  type: string
                  example: Full Body
                description:
                  type: string
                  example: A complete workout for all muscle groups.
                series:
                  type: integer
                  example: 3
                exercises:
                  type: array
                  items:
                    type: object
                    properties:
                      exercise_id:
                        type: integer
                        example: 1
        responses:
          200:
            description: Rutina creada exitosamente
        """
        data = request.get_json()
        routine = self.routine_controller.create_routine(data)
        return ResponseInfo.to_response(routine)

    def search(self):
        """
        Obtiene rutinas por nombre
        ---
        tags:
          - Routine
        parameters:
          - name: name
            in: query
            type: string
            required: true
            example: Full Body Workout
        responses:
          200:
            description: Info obtenida exitosamente
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      routine_id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: Full Body Workout
                      muscular_group:
                        type: string
                        example: Full Body
                      description:
                        type: string
                        example: A complete workout for all muscle groups.
                      series:
                        type: integer
                        example: 3
          400:
            description: Name is required
        """
        name = request.args.get("name")
        if not name:
            return ResponseInfo.to_response((False, "Name is required", 400))
        response = self.routine_controller.search_routine(name)
        return ResponseInfo.to_response((True, response, 200))

    def filter_by_series(self):
        """
        Filtra rutinas por número de series
        ---
        tags:
          - Routine
        parameters:
          - name: series
            in: query
            type: integer
            required: true
            description: Número de series
            x-example: 3
        responses:
          200:
            description: Info obtenida exitosamente
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      routine_id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: Full Body Workout
                      muscular_group:
                        type: string
                        example: Full Body
                      description:
                        type: string
                        example: A complete workout for all muscle groups.
                      series:
                        type: integer
                        example: 3
          400:
            description: Series is required
        """
        series = request.args.get("series", type=int)
        if series is None:
            return ResponseInfo.to_response((False, "Series is required", 400))
        response = self.routine_controller.filter_by_series(series)
        return ResponseInfo.to_response((True, response, 200))
