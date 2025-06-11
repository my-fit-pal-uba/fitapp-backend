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
