from flask import Blueprint, request

from models.response import ResponseInfo
from profile_module.routes.profile_controller import ProfileController


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
            "/register_user_rol",
            view_func=self.post_user_rol,
            methods=["POST"],
        )

    def register_daily_weight(self):
        """
        ---
        tags:
          - Profile
        post:
          summary: Add a role to a user
          description: Adds a new role to a user based on the provided parameters.
          requestBody:
            required: true
            content:
              application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  description: ID of the user
                role:
                  type: string
                  description: Role to add
              required:
                - user_id
                - role
          responses:
            200:
              description: Role added successfully
              content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseInfo'
            400:
              description: Invalid input
        """
        data = request.args.to_dict()
        print(data)
        weight = data.get("weight", None)
        user_id = data.get("user_id", None)

        if not weight or not user_id:
            return ResponseInfo(
                status_code=400,
                message="Weight and user_id are required",
                data=None,
            ).to_dict()

        result = self.profile_controller.register_daily_weight(
            user_id=int(user_id), weight=float(weight)
        )

        return ResponseInfo.to_response(result)

    def register_daily_calories(self):
        """
        ---
        tags:
          - Profile
        post:
          summary: Add a role to a user
          description: Adds a new role to a user based on the provided parameters.
          requestBody:
            required: true
            content:
              application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  description: ID of the user
                role:
                  type: string
                  description: Role to add
              required:
                - user_id
                - role
          responses:
            200:
              description: Role added successfully
              content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseInfo'
            400:
              description: Invalid input
        """
        data = request.args.to_dict()
        calories = data.get("calories", None)
        user_id = data.get("user_id", None)

        if not calories or not user_id:
            return ResponseInfo(
                status_code=400,
                message="Calories and user_id are required",
                data=None,
            ).to_dict()

        result = self.profile_controller.register_daily_calories(
            user_id=int(user_id), calories=float(calories)
        )

        return ResponseInfo.to_response(result)

    def post_user_rol(self):
        """
        ---
        tags:
          - Profile
        post:
          summary: Add a role to a user
          description: Adds a new role to a user based on the provided parameters.
          requestBody:
            required: true
            content:
              application/json:
            schema:
              type: object
              properties:
                user_id:
                  type: integer
                  description: ID of the user
                role:
                  type: string
                  description: Role to add
              required:
                - user_id
                - role
          responses:
            200:
              description: Role added successfully
              content:
            application/json:
              schema:
                $ref: '#/components/schemas/ResponseInfo'
            400:
              description: Invalid input
        """
        data = request.args.to_dict()
        rol_id = data.get("rol_id", None)
        user_id = data.get("user_id", None)

        if not rol_id or not user_id:
            return ResponseInfo(
                status_code=400,
                message="Role and user_id are required",
                data=None,
            ).to_dict()

        result = self.profile_controller.register_rol(
            rol_id=rol_id, user_id=int(user_id)
        )

        return ResponseInfo.to_response(result)
