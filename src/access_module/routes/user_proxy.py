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
        self.user_bp.add_url_rule("/save_profile", view_func=self.save_profile, methods=["POST"])
        self.user_bp.add_url_rule("/get_profile", view_func=self.get_profile, methods=["GET"])

    def info(self):
        """
        Obtiene data de usuario
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
      
    def save_profile(self):
        """
        Guarda perfil de usuario
        ---
        tags:
          - Authentication
        parameters:
          - name: email
            in: query
            type: string
            required: true
            example: usuario@ejemplo,com
          - name: age
            in: query
            type: integer
            required: false
            example: 30
          - name: height
            in: query
            type: number
            required: false
            example: 175
          - name: gender
            in: query
            type: string
            required: false
        responses:
          200:
            description: Info guardada exitosamente
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
          400:
            description: Parámetros inválidos
          404:
            description: Usuario no encontrado
          500:
            description: Error del servidor
        """
        email = request.args.get("email")
        if not email:
            return ResponseInfo.to_response((False, "Email is required", 400))
        
        age = request.args.get("age", type=int)
        height = request.args.get("height", type=int)
        gender = request.args.get("gender", type=str)
        if height <= 0:
            return ResponseInfo.to_response((False, "La estatura debe ser positiva", 400))
        if gender not in ["male", "female", "other"]:
            return ResponseInfo.to_response((False, "Género inválido", 400))
        
        try:
            result = self.user_controller.save_profile(email, age, height, gender)
            return ResponseInfo.to_response((True, "Perfil guardado exitosamente", 200))
        except Exception as e:
            return ResponseInfo.to_response((False, f"Error del servidor: {str(e)}", 500))

    def get_profile(self):
        """
        Obtiene perfil de usuario
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
                    age:
                      type: integer
                      example: 42
                    height:
                      type: integer
                      example: 170
                    gender:
                      type: string
                      example: male
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
        
        response = self.user_controller.get_profile(email)
        return ResponseInfo.to_response((True, response, 200))