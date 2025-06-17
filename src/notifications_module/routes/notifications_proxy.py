from flask import Blueprint, request

from models.response import ResponseInfo
from notifications_module.routes.notifications_controller import NotificationController


class NotificationsProxy:

    def __init__(self, notification_controller: NotificationController):
        self.notification_controller = notification_controller
        self.notifications_bp = Blueprint(
            "notifications", __name__, url_prefix="/notifications"
        )
        self.notifications_bp.add_url_rule(
            "/post_notification",
            view_func=self.post_notification,
            methods=["POST"],
        )
        self.notifications_bp.add_url_rule(
            "/get_notification",
            view_func=self.get_notification,
            methods=["GET"],
        )
        self.register_routes()

    def register_routes(self):
        self.notifications_bp.add_url_rule(
            "/send_email",
            view_func=self.send_email,
            methods=["POST"],
        )

    def send_email(self):
        """
        Obtiene categorías de las comidas
        ---
        tags:
          - notifications
        responses:
          200:
            description: Categorías de comidas obtenidas exitosamente
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
        result = self.notification_controller.send_notification_mail()
        return ResponseInfo.to_response(result)

    def post_notification(self):
        """

        Registra un nuevo plato en la base de datos
        ---
        tags:
          - notifications
        summary: Registra un nuevo plato en la base de datos / Registers a new dish in the database
        description: Crea un nuevo registro de plato con la información nutricional proporcionada / Creates a new dish record with the provided nutritional information
        consumes:
          - application/json
        produces:
          - application/json
        parameters:
          - in: body
            name: body
            description: Nueva notificacion
            required: true
            schema:
              type: object
              required:
                - description
                - user_id
                - date
              properties:
                user_id:
                  type: integer
                  format: int
                  description: ID único del plato
                description:
                  type: string
                  description: Descripción de la notificación
                  example: "Notificación de prueba"
                date:
                  type: string
                  format: date-time
                  description: Fecha de la notificación
                  example: "2023-10-01T12:00:00Z"
                example:
                  description: "Notificación de prueba"
                  date: "2023-10-01T12:00:00Z"
                  user_id: 11
        responses:
          200:
            description: Consumo registrado exitosamente
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "Ensalada César"
          401:
            description: Error en los parametros
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "El plato ya existe en la base de datos"
          500:
            description: Error del servidor
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: false
                error:
                  type: string
                  example: "Error interno del servidor"

        """
        notification = request.get_json()
        print(f"Notification data: {notification}")
        if not notification:
            return ResponseInfo.to_response(
                (False, "Notification data is required", 400)
            )
        result = self.notification_controller.post_notification(notification)
        return ResponseInfo.to_response(result)

    def get_notification(self):
        """
        Get a notification
        ---
        tags:
          - notifications
        parameters:
          - in: query
            name: user_id
            required: true
            schema:
              type: string
            description: The ID of the user to retrieve notifications for
        responses:
          200:
            description: Notification retrieved successfully
            schema:
              type: object
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: string
                  example: "Notification retrieved successfully"
          500:
            description: Error retrieving notification
        """
        user_id = request.args.get("user_id")
        if not user_id:
            return ResponseInfo.to_response((False, "User ID is required", 400))
        result = self.notification_controller.get_notification(int(user_id))

        return ResponseInfo.to_response(result)
