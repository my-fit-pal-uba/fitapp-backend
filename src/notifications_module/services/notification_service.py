import base64
import os
import socket
import ssl

from dotenv import load_dotenv
from notifications_module.services.abstract_notification_service import (
    AbstractNotificationService,
)
from notifications_module.models.notification import Notification
from notifications_module.repository.abstract_notification_repository import (
    AbstractNotificationRepository,
)

import logging

MAILSERVER = "smtp.gmail.com"
PORT = 465




class NotificationService(AbstractNotificationService):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    def __init__(self, notificarion_repository: AbstractNotificationRepository):
        self.notification_repository: AbstractNotificationRepository = (
            notificarion_repository
        )

    def send_notification_email(self, notification_id: int, user_email: str):
        """
        Sends a notification email.
        This method connects to the SMTP server and sends an email with a predefined message.
        """
        path_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(path_dir, ".env")
        load_dotenv(env_path)
        username = os.environ.get("EMAIL_USERNAME")
        logger.info(f"EMAIL_USERNAME en producción: {username}")
        password = os.environ.get("EMAIL_PASSWORD")
        print(f"EMAIL_USERNAME en producción: {username}")
        if not username or not password:
            raise ValueError("Should have set mails configs first")
        notification_message = self.notification_repository.notification_by_id(
            notification_id
        )
        try:
            if not notification_message or notification_message == "":
                notification_message = "Acordate de passar por PeakFit Hoy"
            if self._send_email(
                MAILSERVER, PORT, username, password, notification_message, user_email
            ):
                self.notification_repository.deactivate_notification(notification_id)
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def _send_email(self, mailserver, port, username, password, msg, dst_email):
        try:
            with socket.create_connection((mailserver, port)) as sock:
                context = ssl.create_default_context()
                with context.wrap_socket(
                    sock, server_hostname=mailserver
                ) as secure_sock:
                    self.send_command(secure_sock, "EHLO smtp.gmail.com")

                    self.send_command(secure_sock, "AUTH LOGIN")
                    self.send_command(
                        secure_sock, base64.b64encode(username.encode()).decode()
                    )
                    self.send_command(
                        secure_sock, base64.b64encode(password.encode()).decode()
                    )

                    from_addr = "fitnesspeakfit@gmail.com"
                    to_addr = [dst_email]
                    subject = "Un recordatorio de PeakFit"
                    msg_body = msg

                    self.send_command(secure_sock, f"MAIL FROM: <{from_addr}>")

                    for recipient in to_addr:
                        self.send_command(secure_sock, f"RCPT TO: <{recipient}>")

                    self.send_command(secure_sock, "DATA")

                    email_content = f"Subject: {subject}\r\nTo: {",".join(to_addr)}\r\n\r\n{msg_body}\r\n."
                    self.send_command(secure_sock, email_content)

                    self.send_command(secure_sock, "QUIT")
                    return True
        except ssl.SSLError as e:
            print(f"❌ SSL error: {e}")
            return False
        except Exception as e:
            print(f"❌ General error: {e}")
            return False

    def send_command(self, sock, command):
        sock.send((command + "\r\n").encode("utf-8"))
        response = []
        while True:
            chunk = sock.recv(1024).decode("utf-8")
            response.append(chunk)
            if len(chunk) < 1024:
                break
        msg = "".join(response)
        logger.info(f"SMTP response to '{command}': {msg.strip()}")
        return msg

    def get_notifications(self, user_id: int):
        try:
            """
            Retrieves notifications for a specific user.
            This method simulates fetching notifications by returning a list of dummy notifications.
            """
            return self.notification_repository.get_notifications(user_id)
        except Exception as e:
            print(f"Error retrieving notifications: {e}")
            return []

    def post_notification(self, notification_data: Notification):
        """
        Posts a notification.
        This method simulates posting a notification by returning the provided data.
        """
        try:
            print(f"Posting notification: {notification_data.to_dict()}")
            self.notification_repository.post_notification(notification_data)
        except Exception as e:
            print(f"Error posting notification: {e}")
            return False
