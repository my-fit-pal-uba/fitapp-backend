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
        self.exercise_bp.add_url_rule("/all", view_func=self.get_exercises, methods=["GET"])
        self.exercise_bp.add_url_rule("/filter_by_muscular_group", view_func=self.filter_by_muscular_group, methods=["GET"])
        self.exercise_bp.add_url_rule("/filter_by_place", view_func=self.filter_by_place, methods=["GET"])
        self.exercise_bp.add_url_rule("/filter_by_type", view_func=self.filter_by_type, methods=["GET"])

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
    
