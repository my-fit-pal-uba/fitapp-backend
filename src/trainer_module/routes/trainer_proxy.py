from flask import Blueprint, request, jsonify, make_response

from trainer_module.routes.trainer_controller import TrainerController
from models.response import ResponseInfo


class TrainerProxy:
    def __init__(self, trainer_controller: TrainerController):
        self.trainer_controller = trainer_controller
        self.trainer_bp = Blueprint("trainer", __name__, url_prefix="/trainer")
        self.register_routes()

    def register_routes(self):
        self.trainer_bp.add_url_rule(
            "/register_client", view_func=self.register_client, methods=["POST"]
        )
        self.trainer_bp.add_url_rule(
            "/clients/<int:trainer_id>",
            view_func=self.get_clients_by_trainer,
            methods=["GET"],
        )
        self.trainer_bp.add_url_rule(
            "/share_exercise", view_func=self.share_exercise, methods=["POST"]
        )
        self.trainer_bp.add_url_rule(
            "/share_dish", view_func=self.share_dish, methods=["POST"]
        )
        self.trainer_bp.add_url_rule(
            "/client_dishes", view_func=self.client_dishes, methods=["GET"]
        )
        self.trainer_bp.add_url_rule(
            "/client_exercises", view_func=self.client_exercises, methods=["GET"]
        )

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
            return ResponseInfo.to_response(
                (False, "Entrenador no encontrado o sin clientes", 404)
            )
        return jsonify(result)

    def share_exercise(self):
        """
        Comparte un ejercicio con un cliente
        ---
        tags:
          - Trainer
        parameters:
          - in: body
            name: exercise
            required: true
            schema:
              type: object
              properties:
                client_id:
                  type: integer
                  example: 5
                exercise_id:
                  type: integer
                  example: 10
        responses:
          200:
            description: Ejercicio compartido exitosamente
          400:
            description: Datos inválidos o cliente no encontrado
        """
        data = request.get_json()
        client_id = data.get("client_id")
        exercise_id = data.get("exercise_id")

        if not client_id or not exercise_id:
            return ResponseInfo.to_response((False, "Datos requeridos faltantes", 400))

        result = self.trainer_controller.share_exercise(client_id, exercise_id)
        return ResponseInfo.to_response(result)

    def share_dish(self):
        """
        Comparte un plato con un cliente
        ---
        tags:
          - Trainer
        parameters:
          - in: body
            name: dish
            required: true
            schema:
              type: object
              properties:
                client_id:
                  type: integer
                  example: 5
                dish_id:
                  type: integer
                  example: 10
        responses:
          200:
            description: Plato compartido exitosamente
          400:
            description: Datos inválidos o cliente no encontrado
        """
        data = request.get_json()
        client_id = data.get("client_id")
        dish_id = data.get("dish_id")

        if client_id is None or dish_id is None:
            return ResponseInfo.to_response((False, "Datos requeridos faltantes", 400))

        result = self.trainer_controller.share_dish(client_id, dish_id)
        return ResponseInfo.to_response(result)

    def client_dishes(self):
        """
        Obtiene todos los platos compartidos con un cliente
        ---
        tags:
          - Trainer
        parameters:
          - name: client_id
            in: query
            required: true
            schema:
              type: integer
              example: 5
        responses:
          200:
            description: Lista de platos compartidos con el cliente
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      dish_id:
                        type: integer
                        example: 10
                      dish_name:
                        type: string
                        example: Ensalada César
        """
        client_id = request.args.get("client_id")
        if not client_id:
            return ResponseInfo.to_response((False, "ID de cliente requerido", 400))

        result = self.trainer_controller.client_dishes(client_id)
        return jsonify(result)

    def client_exercises(self):
        """
        Obtiene todos los ejercicios compartidos con un cliente
        ---
        tags:
          - Trainer
        parameters:
          - name: client_id
            in: query
            required: true
            schema:
              type: integer
              example: 5
        responses:
          200:
            description: Lista de ejercicios compartidos con el cliente
            content:
              application/json:
                schema:
                  type: array
                  items:
                    type: object
                    properties:
                      exercise_id:
                        type: integer
                        example: 10
                      exercise_name:
                        type: string
                        example: Flexiones de brazos
        """
        client_id = request.args.get("client_id")
        if not client_id:
            return ResponseInfo.to_response((False, "ID de cliente requerido", 400))

        result = self.trainer_controller.client_exercises(client_id)
        return jsonify(result)
