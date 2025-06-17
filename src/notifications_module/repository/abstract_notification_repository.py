from abc import abstractmethod

from notifications_module.models.notification import Notification


class AbstractNotificationRepository:
    """
    Abstract base class for notification repositories.
    This class defines the interface for notification repositories.
    """

    @abstractmethod
    def get_notifications(self) -> dict:
        """
        Retrieve a notification by its ID.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    @abstractmethod
    def post_notifications(self, notification_data: Notification) -> dict:
        """
        Create a new notification.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")
