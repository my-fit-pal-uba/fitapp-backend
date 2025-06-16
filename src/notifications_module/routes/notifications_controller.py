from notifications_module.services.abstract_notification_service import (
    AbstractNotificationService,
)


class NotificationController:
    def __init__(self, notification_service: AbstractNotificationService):
        self.notification_service = notification_service

    def send_notification_mail(self):
        try:
            return self.notification_service.send_notification_email()
        except Exception as e:
            print(f"Error sending notification email: {e}")
            return False, str(e), 500
