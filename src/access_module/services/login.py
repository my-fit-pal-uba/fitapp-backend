import base64
from datetime import datetime, timedelta
import os
import socket
import ssl

from dotenv import load_dotenv
import jwt
from models.user import User
from access_module.repository.abstract_access_repository import AbstractAccessRepository
from access_module.exceptions.non_existing_user import NonExistingUser

from access_module.services.abstract_login import AbstractAccessService
from access_module.exceptions.invalid_password import InvalidUserPassword
from access_module.exceptions.user_already_exists import UserAlreadyExists
from pytz import timezone


MAILSERVER = "smtp.gmail.com"
PORT = 465

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET", "your_jwt_secret")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 60))


class Login(AbstractAccessService):

    def __init__(self, abstract_access_service: AbstractAccessRepository):
        self.repository: AbstractAccessRepository = abstract_access_service

    def login(self, user_email: str, user_password: str):

        user_data: User = self.repository.get_user_by_email(user_email)

        if not user_data:
            raise NonExistingUser(user_email)

        if user_data.password_hash != user_password:
            raise InvalidUserPassword(user_email)

        return self.create_access_token(user_data)

    def sign_up(self, email: str, password: str, name: str, last_name: str):
        result = self.repository.create_user(email, password, name, last_name)
        if not result:
            raise UserAlreadyExists(email)
        user_data: User = self.repository.get_user_by_email(email)
        return self.create_access_token(user_data)

    def create_access_token(self, user: User):
        dict_user = user.to_dict()
        to_encode = dict_user.copy()
        expire = datetime.now() + timedelta(minutes=JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        argentina_time = datetime.now(
            timezone("America/Argentina/Buenos_Aires")
        ).isoformat()
        to_encode.update({"access_time": argentina_time})
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    def get_users(self):
        return self.repository.get_users()

    def sign_up_google(self, idinfo):
        email = idinfo.get("email")
        name = idinfo.get("given_name")
        last_name = idinfo.get("family_name")
        password = ""

        result = self.repository.create_user(email, password, name, last_name)

        if not result:
            raise UserAlreadyExists(email)

        user_data: User = self.repository.get_user_by_email(email)

        return self.create_access_token(user_data)

    def login_google(self, idinfo):

        email = idinfo.get("email")
        if not email:
            return None

        user_data: User = self.repository.get_user_by_email(email)
        if not user_data:
            # Si el usuario no existe, puedes retornar None o crear el usuario automáticamente
            return None

        return self.create_access_token(user_data)

    def restore_password_mail(self, user_email: str):

        if not user_email:
            raise NonExistingUser(user_email)

        return self._send_notification_email(user_email)

    def _send_notification_email(self, user_email: str):
        """
        Sends a notification email.
        This method connects to the SMTP server and sends an email with a predefined message.
        """
        path_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(path_dir, ".env")
        load_dotenv(env_path)
        username = os.getenv("EMAIL_USERNAME", None)
        password = os.getenv("EMAIL_PASSWORD", None)
        if not username or not password:
            raise ValueError("Should have set mails configs first")
        try:
            return self._send_email(MAILSERVER, PORT, username, password, user_email)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def _send_email(self, mailserver, port, username, password, dst_email):
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
                    subject = "Cambio de contraseña en PeakFit"
                    msg_body = (
                        " "
                        "Te compartimos el link para poder realizar el cambio de contraseña:"
                    )
                    msg_body += "http://localhost:8081/password-reset"

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
        """Send a command to the SMTP server and print the response."""
        sock.send((command + "\r\n").encode("utf-8"))

        response = []
        while True:
            chunk = sock.recv(1024).decode("utf-8")
            response.append(chunk)
            if len(chunk) < 1024:
                break

        msg = "".join(response)
        return msg

    def change_password(self, user_email, new_password):
        if not user_email or not new_password:
            raise NonExistingUser(user_email)

        result = self.repository.change_password(user_email, new_password)
        if not result:
            raise InvalidUserPassword(user_email)

        return True
