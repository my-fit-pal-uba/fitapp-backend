from flask import Blueprint, request

from access_module.routes.login_controller import LoginController
from models.response import ResponseInfo


### Aca agrego la logica dependiente de flasl
class LoginProxy:
    def __init__(self, login_controller: LoginController):
        self.login_controller: LoginController = login_controller
        self.login_bp = Blueprint("login", __name__, url_prefix="/access")
        self.register_routes()

    def register_routes(self):
        self.login_bp.add_url_rule("/login", view_func=self.login, methods=["GET"])
        self.login_bp.add_url_rule("/signup", view_func=self.sign_up, methods=["POST"])
        # self.login_bp.add_url_rule("/users", view_func=self.get_users, methods=["GET"])

    def login(self):
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
            example: usuario_ejemplo
          - name: password
            in: query
            type: string
            required: true
            example: contraseñaSegura123
        responses:
          200:
            description: Login exitoso
            schema:
              type: object
              properties:
                token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                user_id:
                  type: integer
                  example: 42
          401:
            description: Credenciales inválidas
          500:
            description: Error del servidor
        """
        data = request.args.to_dict()
        user_email = data.get("email", None)
        user_password = data.get("password", None)
        if not user_email or not user_password:
            return ResponseInfo.to_response(
                (False, "Email and password are required", 400)
            )

        responde = self.login_controller.login(user_email, user_password)

        return ResponseInfo.to_response(responde)

    def sign_up(self):
        """
        Autentica a un usuario existente
        ---
        tags:
          - Authentication
        parameters:
          - name: body
            in: body
            type: string
            required: true
            example: {
                        "email": "juan.perez@ejemplo.com",
                        "password": "PasswordSeguro123!",
                        "name": "Juan",
                        "last_name": "Perez"
                    }
        responses:
          200:
            description: Login exitoso
            schema:
              type: object
              properties:
                token:
                  type: string
                  example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
                user_id:
                  type: integer
                  example: 42
          401:
            description: Credenciales inválidas
          500:
            description: Error del servidor
        """
        if not request.is_json:
            return ResponseInfo.to_response((False, "Request body must be JSON", 400))

        data = request.get_json()
        user_email = data.get("email", None)
        user_password = data.get("password", None)
        user_name = data.get("name", "")
        user_last_name = data.get("last_name", "")
        if not user_email or not user_password:
            return ResponseInfo.to_response(
                (False, "Email and password are required", 400)
            )
        responde = self.login_controller.sign_up(
            user_email, user_password, user_name, user_last_name
        )
        return ResponseInfo.to_response(responde)
