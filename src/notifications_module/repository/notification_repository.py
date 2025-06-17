from notifications_module.repository.abstract_notification_repository import (
    AbstractNotificationRepository,
)

from typing import List, Optional  # noqa: F401
import psycopg2  # type: ignore
from psycopg2.extras import DictCursor  # type: ignore # noqa: F401

from notifications_module.models.notification import Notification  # type: ignore


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
        query = """
            SELECT 
                id, 
                user_id,
                description,
                date, 
                active
            FROM notifications
            WHERE user_id = %s
        """
        try:
            with (
                self.get_connection() as conn,
                conn.cursor(cursor_factory=DictCursor) as cursor,
            ):
                cursor.execute(query, (user_id,))
                records = cursor.fetchall()
                return [
                    Notification(
                        id=record["id"],
                        description=record["description"],
                        date=record["date"],
                        user_id=record["user_id"],
                    )
                    for record in records
                ]
        except psycopg2.Error:
            return []

    def post_notification(self, notification_data: Notification):
        pass
