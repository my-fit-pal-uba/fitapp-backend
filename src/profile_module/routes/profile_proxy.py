from flask import Blueprint, request

from models.response import ResponseInfo
from src.profile_module.routes.profile_controller import ProfileController


### Aca agrego la logica dependiente de flasl
class ProfileProxy:
    def __init__(self, login_controller: ProfileController):
        self.login_controller: ProfileController = login_controller
        self.login_bp = Blueprint("profile", __name__, url_prefix="/profile")
        self.register_routes()

    def register_routes(self):
        self.login_bp.add_url_rule(
            "/add_role", view_func=self.add_role, methods=["POST"]
        )
        self.login_bp.add_url_rule(
            "/register_user_weight",
            view_func=self.register_user_weight,
            methods=["POST"],
        )

        """
        ---
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

    def register_user_weight(self):
        """ """
        data = request.args.to_dict()
        print(data)
        return ResponseInfo(
            status_code=200,
            message="User weight registered successfully",
            data=data,
        ).to_dict()
