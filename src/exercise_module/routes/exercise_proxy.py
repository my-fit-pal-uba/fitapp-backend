from flask import Blueprint, request

from exercise_module.routes.exercise_controller import ExerciseController
from models.response import ResponseInfo


class ExerciseProxy:
    def __init__(self, exercise_controller: ExerciseController):
        self.exercise_controller = exercise_controller
        self.exercise_bp = Blueprint("exercise", __name__, url_prefix="/exercises")
        self.register_routes()

    def register_routes(self):
        self.exercise_bp.add_url_rule("/search", view_func=self.search, methods=["GET"])
        self.exercise_bp.add_url_rule(
            "/all", view_func=self.get_exercises, methods=["GET"]
        )
        self.exercise_bp.add_url_rule(
            "/filter_by_muscular_group",
            view_func=self.filter_by_muscular_group,
            methods=["GET"],
        )
        self.exercise_bp.add_url_rule(
            "/filter_by_place", view_func=self.filter_by_place, methods=["GET"]
        )
        self.exercise_bp.add_url_rule(
            "/filter_by_type", view_func=self.filter_by_type, methods=["GET"]
        )
        self.exercise_bp.add_url_rule(
            "/register_series", view_func=self.register_series, methods=["POST"]
        )
        self.exercise_bp.add_url_rule(
            "/<int:exercise_id>/rate", view_func=self.rate_exercise, methods=["POST"]
        )


    def search(self):
        """
        Obtiene ejercicios por nombre
        ---
        tags:
          - Exercise
        parameters:
          - name: name
            in: query
            type: string
            required: true
            example: push up
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
                      exercise_id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: Push Up
                      description:
                        type: string
                        example: A basic push-up exercise.
          400:
            description: Name is required
        """
        name = request.args.get("name")
        if not name:
            return ResponseInfo.to_response((False, "Name is required", 400))
        response = self.exercise_controller.search_exercises(name)
        return ResponseInfo.to_response((True, response, 200))

    def get_exercises(self):
        """
        Obtiene todos los ejercicios
        ---
        tags:
          - Exercise
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
                      exercise_id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: Push Up
                      description:
                        type: string
                        example: A basic push-up exercise.
          500:
            description: Internal Server Error
        """
        response = self.exercise_controller.get_exercises()
        return ResponseInfo.to_response((True, response, 200))

    def filter_by_muscular_group(self):
        """
        Filtra ejercicios por grupo muscular
        ---
        tags:
          - Exercise
        parameters:
          - name: muscular_group
            in: query
            type: string
            required: true
            example: chest
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
                      exercise_id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: Push Up
                      description:
                        type: string
                        example: A basic push-up exercise.
          400:
            description: Muscular group is required
        """
        muscular_group = request.args.get("muscular_group")
        if not muscular_group:
            return ResponseInfo.to_response((False, "Muscular group is required", 400))
        response = self.exercise_controller.filter_by_muscular_group(muscular_group)
        return ResponseInfo.to_response((True, response, 200))

    def filter_by_place(self):
        """
        Filtra ejercicios por lugar
        ---
        tags:
          - Exercise
        parameters:
          - name: place
            in: query
            type: string
            required: true
            example: gym
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
                      exercise_id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: Push Up
                      description:
                        type: string
                        example: A basic push-up exercise.
          400:
            description: Place is required
        """
        place = request.args.get("place")
        if not place:
            return ResponseInfo.to_response((False, "Place is required", 400))
        response = self.exercise_controller.filter_by_place(place)
        return ResponseInfo.to_response((True, response, 200))

    def filter_by_type(self):
        """
        Filtra ejercicios por tipo
        ---
        tags:
          - Exercise
        parameters:
          - name: type
            in: query
            type: string
            required: true
            example: strength
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
                      exercise_id:
                        type: integer
                        example: 1
                      name:
                        type: string
                        example: Push Up
                      description:
                        type: string
                        example: A basic push-up exercise.
          400:
            description: Type is required
        """
        type_ = request.args.get("type")
        if not type_:
            return ResponseInfo.to_response((False, "Type is required", 400))
        response = self.exercise_controller.filter_by_type(type_)
        return ResponseInfo.to_response((True, response, 200))

    def register_series(self):
        """
        Guarda Series de un ejercicio realizadas por un usuario
        ---
        tags:
          - Exercise
        consumes:
          - application/json
        parameters:
          - name: user_id
            in: query
            type: integer
            required: true
            example: 12
          - name: exercise_id
            in: query
            type: integer
            required: false
            example: 4
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - series
              properties:
                series:
                  type: array
                  items:
                    type: object
                    required:
                      - repetitions
                      - weight
                    properties:
                      repetitions:
                        type: integer
                        example: 10
                      weight:
                        type: number
                        format: float
                        example: 75.5
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
            description: Usuario  o ejercicio no encontrado
          500:
            description: Error del servidor
        """
        user_id = request.args.get("user_id", type=int)
        exercise_id = request.args.get("exercise_id", type=int)

        if not user_id or not exercise_id:
            return ResponseInfo.to_response(
                (False, "User ID and Exercise ID are required", 400)
            )

        data = request.get_json()
        if not data or "series" not in data:
            return ResponseInfo.to_response(
                (False, "Request body must contain 'series' list", 400)
            )

        series = data["series"]
        if not isinstance(series, list) or len(series) == 0:
            return ResponseInfo.to_response(
                (False, "'series' must be a non-empty list", 400)
            )

        response = self.exercise_controller.register_series(
            user_id, exercise_id, series
        )

        return ResponseInfo.to_response((True, response, 200))
    
    def rate_exercise(self, exercise_id):
      '''
      Registra la calificación de un ejercicio
      ---
      tags:
        - Exercise
      consumes:
        - application/json
      parameters:
        - in: path
          name: exercise_id
          schema:
            type: integer
          required: true
          description: ID del ejercicio a calificar
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
          description: Ejercicio no encontrado
        500:
          description: Error del servidor
      '''

      print(request.get_json())

      user_id = request.json.get("user_id")
      rating = request.json.get("rating")
      if not user_id or not rating:
        return ResponseInfo.to_response(
          (False, "User ID and rating are required", 400)
      )

      import logging
      logging.basicConfig(level=logging.DEBUG)

      logging.debug("Request JSON: %s", request.get_json())

      if not isinstance(rating, int) or rating < 1 or rating > 5:
        return ResponseInfo.to_response(
          (False, "Rating must be an integer between 1 and 5", 400)
      )

      return ResponseInfo.to_response(
        self.exercise_controller.rate_exercise(user_id, exercise_id, rating)
      )
