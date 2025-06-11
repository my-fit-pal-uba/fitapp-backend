from flask import Blueprint, request
from diet_module.routes.diet_controller import DietController
from models.response import ResponseInfo


class DietProxy:
    def __init__(self, diet_service):
        self.diet_service: DietController = diet_service
        self.diet_bp = Blueprint("diet", __name__, url_prefix="/diet")
        self.register_routes()

    def register_routes(self):
        self.diet_bp.add_url_rule(
            "/get_diets", view_func=self.get_diets, methods=["GET"]
        )
        self.diet_bp.add_url_rule(
            "/create_diet", view_func=self.create_diet, methods=["POST"]
        )
        self.diet_bp.add_url_rule(
            "/add_dish", view_func=self.add_dish, methods=["POST"]
        )

    def get_diets(self):
        """
        Obtiene categorías de las comidas
        ---
        tags:
          - diets
        parameters:
          - name: user_id
            in: query
            type: int
            example: 1
        responses:
          200:
            description: Recupera todas las dietas disponibles
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
        user_id = request.args.get("user_id", None)
        if not user_id:
            return ResponseInfo.to_response((False, "User ID is required", 400))
        result = self.diet_service.get_diets(user_id)
        if result is None:
            return {"message": "No diets found"}, 500
        return ResponseInfo.to_response(result)

    def update_diet(self, user_id, diet_data):
        return self.diet_service.update_diet(user_id, diet_data)

    def delete_diet(self, user_id):
        return self.diet_service.delete_diet(user_id)

    def create_diet(self):
        """
        Crea una nueva dieta
        ---
        tags:
          - diets
        parameters:
          - name: user_id
            in: query
            type: int
            example: 1
          - name: diet_data
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Dieta Mediterránea"
                observation:
                  type: string
                  example: "Enfocada en el consumo de frutas, verduras, granos enteros, pescado y aceite de oliva."
        responses:
          201:
            description: Dieta creada exitosamente
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
          500:
            description: Error del servidor
        """
        user_id = request.args.get("user_id", None)
        if not user_id:
            return ResponseInfo.to_response((False, "User ID is required", 400))

        diet_data = request.json
        if not diet_data or not isinstance(diet_data, dict):
            return ResponseInfo.to_response((False, "Invalid diet data", 400))

        result = self.diet_service.create_diet(user_id, diet_data)
        if result is None:
            return {"message": "Failed to create diet"}, 500

        return ResponseInfo.to_response(result)

    def add_dish(self):
        """
        Agrega un plato a una dieta
        ---
        tags:
          - diets
        parameters:
          - name: diet_id
            in: query
            type: int
            example: 1
          - name: dish_id
            in: body
            required: true
            schema:
              type: object
              properties:
                dish_id:
                  type: int
                  example: 3
                meal_category_id:
                  type: int
                  example: 2
                serving_size_g:
                  type: float
                  example: 150.0
        responses:
          201:
            description: Plato agregado exitosamente a la dieta
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
          500:
            description: Error del servidor
        """
        diet_id = request.args.get("diet_id", None)
        if not diet_id:
            return ResponseInfo.to_response((False, "Diet ID is required", 400))

        dish_data = request.json
        if not dish_data:
            return ResponseInfo.to_response((False, "Dish is required", 400))

        result = self.diet_service.add_dish(diet_id, dish_data)
        if result is None:
            return {"message": "Failed to add dish to diet"}, 500

        return ResponseInfo.to_response(result)
