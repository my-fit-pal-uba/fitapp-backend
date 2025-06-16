class AbstractNotificationService:

    def send_notification_email(self):
        """
        Sends a notification email.
        This method should be implemented by subclasses to define the specific email sending logic.
        """
        raise NotImplementedError("Subclasses must implement this method.")
