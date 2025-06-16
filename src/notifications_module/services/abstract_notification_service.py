class AbstractNotificationService:

    def send_notification_email(self):
        """
        Sends a notification email.
        This method should be implemented by subclasses to define the specific email sending logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    def get_notifications(self, user_id: int):
        """
        Retrieves notifications.
        This method should be implemented by subclasses to define how notifications are fetched.
        """
        raise NotImplementedError("Subclasses must implement this method.")
