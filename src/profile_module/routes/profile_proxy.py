from flask import Blueprint, request

from models.response import ResponseInfo
from profile_module.routes.profile_controller import ProfileController
from models.profile import Profile


### Aca agrego la logica dependiente de flasl
class ProfileProxy:
    def __init__(self, profile_controller: ProfileController):
        self.profile_controller: ProfileController = profile_controller
        self.profile_bp = Blueprint("profile", __name__, url_prefix="/profiles")
        self.register_routes()

    def register_routes(self):
        self.profile_bp.add_url_rule(
            "/post_daily_weight",
            view_func=self.post_daily_weight,
            methods=["POST"],
        )
        self.profile_bp.add_url_rule(
            "/post_daily_calories",
            view_func=self.post_daily_calories,
            methods=["POST"],
        )
        self.profile_bp.add_url_rule(
            "/post_user_rol",
            view_func=self.post_user_rol,
            methods=["POST"],
        )

        self.profile_bp.add_url_rule(
            "/save_profile", view_func=self.save_profile, methods=["POST"]
        )
        self.profile_bp.add_url_rule(
            "/get_profile", view_func=self.get_profile, methods=["GET"]
        )
        self.profile_bp.add_url_rule(
            "/get_user_rols", view_func=self.get_user_rols, methods=["GET"]
        )

    def post_daily_weight(self):
        """
        Autentica a un usuario existente
        ---
        tags:
          - Profile
        parameters:
          - name: body
            in: body
            type: string
            required: true
            example: {
                        "user_id": "1",
                        "weight": "80.5"
                    }
        responses:
          200:
            description: Peso registrado exitosamente
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  example: 42
                weight:
                  type: float
                  example: 42
          500:
            description: Error inesperado del servidor
        """

        data = request.get_json()
        weight = data.get("weight", None)
        user_id = data.get("user_id", None)

        if not weight or not user_id:
            return ResponseInfo.to_response(
                (False, "Weight and user_id are required", 400)
            )
        result = self.profile_controller.register_daily_weight(
            user_id=int(user_id), weight=float(weight)
        )

        return ResponseInfo.to_response(result)

    def post_daily_calories(self):
        """

        Autentica a un usuario existente
        ---
        tags:
          - Profile
        parameters:
          - name: body
            in: body
            type: string
            required: true
            example: {
                        "user_id": "1",
                        "calories": "80.5"
                    }
        responses:
          200:
            description: Peso registrado exitosamente
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  example: 42
                calories:
                  type: float
                  example: 42
          500:
            description: Error inesperado del servidor
        """

        data = request.get_json()
        calories = data.get("calories", None)
        user_id = data.get("user_id", None)

        if not calories or not user_id:
            return ResponseInfo.to_response(
                (False, "Calories and user_id are required", 400)
            )
        result = self.profile_controller.register_daily_calories(
            user_id=int(user_id), calories=float(calories)
        )

        return ResponseInfo.to_response(result)

    def save_profile(self):
        """
        Guarda perfil de usuario
        ---
        tags:
          - Profile
        parameters:
          - name: user_id
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
        user_id = request.args.get("user_id")
        if not user_id:
            return ResponseInfo.to_response((False, "user_id is required", 400))

        age = request.args.get("age", type=int)
        height = request.args.get("height", type=int)
        gender = request.args.get("gender", type=str)
        if height <= 0:
            return ResponseInfo.to_response(
                (False, "La estatura debe ser positiva", 400)
            )
        if gender not in ["male", "female", "other"]:
            return ResponseInfo.to_response((False, "Género inválido", 400))

        profile = Profile(user_id=user_id, age=age, height=height, gender=gender)
        try:
            result = self.profile_controller.save_profile(profile)
            if not result:
                return ResponseInfo.to_response((False, "Usuario no encontrado", 404))
            return ResponseInfo.to_response(result)
        except Exception as e:
            return ResponseInfo.to_response(
                (False, f"Error del servidor: {str(e)}", 500)
            )

    def get_profile(self):
        """
        Obtiene perfil de usuario
        ---
        tags:
          - Profile
        parameters:
          - name: user_id
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
            description: user_id es requerido
          404:
            description: Usuario no encontrado
          500:
            description: Error del servidor
        """
        user_id = request.args.get("user_id")
        if not user_id:
            return ResponseInfo.to_response((False, "user_id is required", 400))

        response = self.profile_controller.get_profile(user_id)
        if not response:
            return ResponseInfo.to_response((False, "Usuario no encontrado", 404))
        return ResponseInfo.to_response(response)

    def get_user_rols(self):
        """
        Obtiene roles de usuario
        ---
        tags:
          - Profile
        parameters: []
        responses:
          200:
            description: Roles obtenidos exitosamente
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
        response = self.profile_controller.get_user_rols()
        return ResponseInfo.to_response(response)

    def post_user_rol(self):
        """
        Autentica a un usuario existente
        ---
        tags:
          - Profile
        parameters:
          - name: body
            in: body
            type: string
            required: true
            example: {
                        "user_id": "1",
                        "rol_id": "Perez"
                    }
        responses:
          200:
            description: Login exitoso
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  example: 42
                rol_id:
                  type: integer
                  example: 42
          401:
            description: Credenciales inválidas
          500:
            description: Error del servidor
        """
        data = request.get_json()
        rol_id = data.get("rol_id", None)
        user_id = data.get("user_id", None)

        if not rol_id or not user_id:
            return ResponseInfo(
                status_code=400,
                message="Role and user_id are required",
                data=None,
            ).to_dict()

        result = self.profile_controller.register_user_rol(
            rol_id=int(rol_id), user_id=int(user_id)
        )

        return ResponseInfo.to_response(result)
