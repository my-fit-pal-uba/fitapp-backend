from notifications_module.repository.abstract_notification_repository import (
    AbstractNotificationRepository,
)

from typing import List, Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor

from src.notifications_module.models.notification import Notification  # type: ignore


class NotificationRepository(AbstractNotificationRepository):
    def __init__(self, db_config=None):
        self.db_config = db_config or {
            "host": "db",
            "database": "app_db",
            "user": "app_user",
            "password": "app_password",
            "port": "5432",
        }

    def get_connection(self):
        return psycopg2.connect(**self.db_config)

    def get_notifications(self, user_id):
        pass

    def post_notification(self, notification_data: Notification):
        pass
