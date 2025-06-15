from flask import Blueprint, request, jsonify, make_response

from trainer_module.routes.trainer_controller import TrainerController
from models.response import ResponseInfo


class TrainerProxy:
    def __init__(self, trainer_controller: TrainerController):
        self.trainer_controller = trainer_controller
        self.trainer_bp = Blueprint("trainer", __name__, url_prefix="/trainer")
        self.register_routes()

    def register_routes(self):
        self.trainer_bp.add_url_rule("/register_client", view_func=self.register_client, methods=["POST"])
        self.trainer_bp.add_url_rule("/clients/<int:trainer_id>", view_func=self.get_clients_by_trainer, methods=["GET"])
       
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


    def get_clients_by_trainer(self, trainer_id: int):
        """
        Obtiene todos los clientes asociados a un entrenador
        ---
        tags:
          - Trainer
        parameters:
          - name: trainer_id
            in: path
            required: true
            schema:
              type: integer
              example: 7
        responses:
          200:
            description: Lista de clientes asociados
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      user_id:
                        type: integer
                        example: 3
                      first_name:
                        type: string
                        example: Juan
                      last_name:
                        type: string
                        example: Pérez
          404:
            description: Entrenador no encontrado o sin clientes
        """
        result = self.trainer_controller.get_clients_by_trainer(trainer_id)
        if result is None:
            return ResponseInfo.to_response((False, "Entrenador no encontrado o sin clientes", 404))
        return jsonify(result)