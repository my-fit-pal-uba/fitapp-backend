from flask import Blueprint
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
