from flask import Blueprint, request

from trainer_module.routes.trainer_controller import TrainerController
from models.response import ResponseInfo

class TrainerProxy:
    def __init__(self, trainer_controller: TrainerController):
        self.trainer_controller = trainer_controller
        self.trainer_bp = Blueprint("trainer", __name__, url_prefix="/trainer")
        self.register_routes()

    def register_routes(self):
        self.trainer_bp.add_url_rule("/register_client", view_func=self.register_client, methods=["POST"])
       
    def register_client(self):
        """
        Registra un cliente a un entrenador
        ---
        tags:
          - Trainer
        parameters:
          - in: body
            name: client
            required: true
            schema:
              type: object
              properties:
                patient_key:
                  type: string
                  example: JuanPerez#123
                trainer_id:
                  type: integer
                  example: 7
        responses:
          200:
            description: Cliente vinculado exitosamente
          400:
            description: Datos inválidos o paciente no encontrado
        """
        data = request.get_json()
        patient_key = data.get("patient_key")
        trainer_id = data.get("trainer_id")

        if not patient_key or not trainer_id:
            return ResponseInfo.to_response((False, "Datos requeridos faltantes", 400))

        result = self.trainer_controller.register_client(patient_key, trainer_id)
        return ResponseInfo.to_response(result)