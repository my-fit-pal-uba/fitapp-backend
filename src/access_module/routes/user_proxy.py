from flask import Blueprint, request

from access_module.routes.user_controller import UserController
from models.response import ResponseInfo

class UserProxy:
    def __init__(self, user_controller: UserController):
        self.user_controller = user_controller
        self.user_bp = Blueprint("user", __name__, url_prefix="/users")
        self.register_routes()

    def register_routes(self):
        self.user_bp.add_url_rule("/info", view_func=self.info, methods=["GET"])

    def info(self):
        """
        Autentica a un usuario existente
        ---
        tags:
          - Authentication
        parameters:
          - name: email
            in: query
            type: string
            required: true
            example: usuario@ejemplo,com
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
                  type: object
                  properties:
                    user_id:
                      type: integer
                      example: 42
                    username:
                      type: string
                      example: usuario_ejemplo
                    email:
                      type: string
                      example: pepe@gmail
                    first_name:
                      type: string
                      example: Pepe
                    last_name:
                      type: string
                      example: Perez
                    is_active:
                      type: boolean
                      example: true
          400:
            description: Email es requerido
          404:
            description: Usuario no encontrado
          500:
            description: Error del servidor
        """
        email = request.args.get("email")
        if not email:
            return ResponseInfo.to_response((False, "Email is required", 400))
        
        response = self.user_controller.get_user_info(email)
        return ResponseInfo.to_response((True, response, 200))