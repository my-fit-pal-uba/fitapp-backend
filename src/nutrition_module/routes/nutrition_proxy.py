from venv import logger
from flask import Blueprint, request  # type: ignore
from nutrition_module.routes.nutrition_controller import NutritionController
from models.response import ResponseInfo


class NutritionProxy:

    def __init__(self, nutrition_controller):
        self.nutrition_controller: NutritionController = nutrition_controller
        self.nutrition_bp = Blueprint("nutritions", __name__, url_prefix="/nutrition")
        self.register_routes()

    def register_routes(self):
        self.nutrition_bp.add_url_rule(
            "/get_meal_categories",
            view_func=self.get_meal_categories,
            methods=["GET"],
        )
        self.nutrition_bp.add_url_rule(
            "/post_dish",
            view_func=self.post_dish,
            methods=["POST"],
        )

    def get_meal_categories(self):
        """
        Obtiene categorías de las comidas
        ---
        tags:
          - nutrition
        responses:
          200:
            description: Categorías de comidas obtenidas exitosamente
            schema:
              type: object
              properties:
            success:
              type: boolean
              example: true
            data:
              type: array
              items:
                type: string
          500:
            description: Error del servidor
        """
        response = self.nutrition_controller.get_meal_categories()
        return ResponseInfo.to_response(response)

    def post_dish(self):
        """
        Registra un nuevo plato en la base de datos
        ---
        tags:
          - nutrition
        summary: Registra un nuevo plato en la base de datos / Registers a new dish in the database
        description: Crea un nuevo registro de plato con la información nutricional proporcionada / Creates a new dish record with the provided nutritional information
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            description: Objeto Plato que necesita ser registrado
            required: true
            schema:
              type: object
              required:
                - id
                - name
                - description
                - calories
                - proteins
                - carbs
                - fats
                - weight
                - id_dish_category
              properties:
                id:
                  type: integer
                  format: int64
                  description: ID único del plato
                name:
                  type: string
                  description: Nombre del plato
                description:
                  type: string
                  description: Descripción detallada del plato
                calories:
                  type: number
                  format: float
                  description: Calorías del plato (en kcal)
                proteins:
                  type: number
                  format: float
                  description: Contenido de proteínas (en gramos)
                carbohydrates:
                  type: number
                  format: float
                  description: Contenido de carbohidratos (en gramos)
                fats:
                  type: number
                  format: float
                  description: Contenido de grasas (en gramos)
                weight:
                  type: number
                  format: float
                  description: Peso total del plato (en gramos)
                id_dish_category:
                  type: number
                  format: int
                  description: Id de la categoria del plato
        responses:
          200:
            description: Plato registrado exitosamente
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "Ensalada César"
          401:
            description: El plato ya existe
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "El plato ya existe en la base de datos"
          500:
            description: Error del servidor
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "Error interno del servidor"
        """
        try:
            dish_json = request.get_json()
            if not dish_json:
                return ResponseInfo.to_response((None, "Invalid input data", 500))
            result = self.nutrition_controller.post_dish(dish_json)
            return ResponseInfo.to_response(result)
        except Exception as e:
            logger.error(f"Error registering dish: {e}")
            return ResponseInfo.to_response((None, "Error registering dish", 500))
