from flask import Blueprint

from models.response import ResponseInfo
from notifications_module.routes.notifications_controller import NotificationController


class NotificationsProxy:

    def __init__(self, notification_controller: NotificationController):
        self.notification_controller = notification_controller
        self.notifications_bp = Blueprint(
            "notifications", __name__, url_prefix="/notifications"
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

        # self._send_email(mailserver, port)
        # return ResponseInfo.to_response((True, "Email sent successfully", 200))
        result = self.notification_controller.send_notification_mail()
        return ResponseInfo.to_response(result)
