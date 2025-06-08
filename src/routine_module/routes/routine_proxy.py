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
        self.routine_bp.add_url_rule("/all", view_func=self.all, methods=["GET"])
        self.routine_bp.add_url_rule(
            "/filter_by_series", view_func=self.filter_by_series, methods=["GET"]
        )
        self.routine_bp.add_url_rule(
            "/<int:routine_id>/rate", view_func=self.rate_routine, methods=["POST"]
        )
        self.routine_bp.add_url_rule(
            "/ratings", view_func=self.get_ratings, methods=["GET"]
        )
        self.routine_bp.add_url_rule(
            "/average-ratings", view_func=self.get_average_ratings, methods=["GET"]
        )
        self.routine_bp.add_url_rule(
            "/register", view_func=self.register, methods=["POST"]
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

    def all(self):
        """
        Obtiene todas las rutinas
        ---
        tags:
          - Routine
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
        """
        response = self.routine_controller.get_all_routines()
        return ResponseInfo.to_response((True, response, 200))

    def rate_routine(self, routine_id):
        """
        Registra la calificación de una Rutina
        ---
        tags:
          - Routine
        consumes:
          - application/json
        parameters:
          - in: path
            name: routine_id
            schema:
              type: integer
            required: true
            description: ID de la rutina a calificar
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - user_id
                - rating
              properties:
                user_id:
                  type: integer
                  example: 15
                rating:
                  type: integer
                  minimum: 1
                  maximum: 5
                  example: 4
        responses:
          200:
            description: Calificación registrada exitosamente
          400:
            description: Datos inválidos o faltantes
          404:
            description: Rutina no encontrada
          500:
            description: Error del servidor
        """

        print(request.get_json())

        user_id = request.json.get("user_id")
        rating = request.json.get("rating")
        if not user_id or not rating:
            return ResponseInfo.to_response(
                (False, "User ID and rating are required", 400)
            )

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return ResponseInfo.to_response(
                (False, "Rating must be an integer between 1 and 5", 400)
            )

        return ResponseInfo.to_response(
            self.routine_controller.rate_routine(user_id, routine_id, rating)
        )

    def get_ratings(self):
        """
        Obtiene las calificaciones de las rutinas
        ---
        tags:
          - Routine
        parameters:
          - name: user_id
            in: query
            type: integer
            required: true
            description: ID del usuario
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
                      rating:
                        type: integer
                        example: 4
          400:
            description: User ID is required
          500:
            description: Internal Server Error
        """
        user_id = request.args.get("user_id", type=int)
        if not user_id:
            return ResponseInfo.to_response((False, "User ID is required", 400))

        response = self.routine_controller.get_ratings(user_id)
        return ResponseInfo.to_response((True, response, 200))

    def get_average_ratings(self):
        """
        Obtiene las calificaciones promedio de los ejercicios
        ---
        tags:
          - Routine
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
                      rating:
                        type: integer
                        example: 4
          400:
            description: User ID is required
          500:
            description: Internal Server Error
        """
        response = self.routine_controller.get_average_ratings()
        return ResponseInfo.to_response((True, response, 200))
  
    def register(self):
        """
        Guarda Series de un ejercicio realizadas por un usuario
        ---
        tags:
          - Routine
        consumes:
          - application/json
        parameters:
          - name: user_id
            in: query
            type: integer
            required: true
            example: 12
          - name: routine_id
            in: query
            type: integer
            required: false
            example: 4
        responses:
          200:
            description: Info guardada exitosamente
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
          404:
            description: Usuario  o rutina no encontrado
          500:
            description: Error del servidor
        """
        user_id = request.args.get("user_id", type=int)
        routine_id = request.args.get("routine_id", type=int)

        if not user_id or not routine_id:
            return ResponseInfo.to_response(
                (False, "User ID and routine ID are required", 400)
            )

        response = self.routine_controller.register(
            user_id, routine_id
        )

        return ResponseInfo.to_response((True, response, 200))