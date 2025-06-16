import base64
import os
import socket
import ssl

from dotenv import load_dotenv
from notifications_module.services.abstract_notification_service import (
    AbstractNotificationService,
)

MAILSERVER = "smtp.gmail.com"
PORT = 465


class NotificationService(AbstractNotificationService):
    def __init__(self):
        pass

    def send_notification_email(self):
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
            raise ValueError(
                f"Email username and password must be set in environment variables. "
                f"Check the variables in the environment where you run this script. "
                f"File: {os.path.abspath(__file__)}"
            )
        self._send_email(MAILSERVER, PORT, username, password)
        return True, "Email sent successfully", 200

    def _send_email(self, mailserver, port, username, password):
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
                    to_addr = ["jcastrom@fi.uba.ar"]
                    subject = "Invitación al gimnasio"
                    msg_body = """
                    *🏳️‍🌈 ¡Tu Mejor Versión te Espera en Fitness Peak Fit! 🏳️‍🌈*  

                    *💪 El primer gimnasio gay-friendly donde el sudor se mezcla con el orgullo*  

                    En *Fitness Peak Fit* no solo moldeamos cuerpos - construimos *comunidad, confianza y autoestima* en un espacio 100% libre de prejuicios.  

                    ### 🌟 *Nuestros diferenciales rainbow:*  
                    ✅ *Zonas diseñadas para tu comodidad* (vestuarios gender-neutral, área lounge)  
                    ✅ *Clases que desafían estereotipos*:  
                      - 🧘‍♂️ Yoga Drag (viernes glam)  
                      - 🥊 Boxeo sin Machismos  
                      - 💃 Cardio Beyoncé  
                    ✅ *Equipo especializado en salud LGBTQ+*  
                    ✅ *Sábados Sociales* (después del entrenamiento: jugos, música y networking)  

                    ### 🔥 *OFERTA DE LANZAMIENTO*  
                    *30% OFF* en tu primera membresía + *1 clase gratis* al usar el código: *#RAINBOWPEAK*  

                    📍 *Donde estamos*: Calle Céspedes 2940
                    📩 *Reservas*: fitnesspeakfit@gmail.com
                    ⏰ *Horario extendido*: 6AM-11PM (porque sabemos de after-offices)  

                    *#NoEsGymEsRevolución #FitnessSinArmarios*  

                    "En Fitness Peak Fit no preguntamos cómo te identificas - preguntamos qué meta quieres lograr"  

                    ---  
                    ✨ *Bonus: Presentando este mail en recepción, **tu primera suplementación post-entreno es cortesía de la casa*.  

                    *¡Te estamos esperando con los brazos (y mancuernas) abiertos!* 💪🌈
                    """

                    self.send_command(secure_sock, f"MAIL FROM: <{from_addr}>")

                    for recipient in to_addr:
                        self.send_command(secure_sock, f"RCPT TO: <{recipient}>")

                    self.send_command(secure_sock, "DATA")

                    email_content = f"Subject: {subject}\r\nTo: {",".join(to_addr)}\r\n\r\n{msg_body}\r\n."
                    self.send_command(secure_sock, email_content)

                    self.send_command(secure_sock, "QUIT")

            print("✅ Email sent successfully!")

        except ssl.SSLError as e:
            print(f"❌ SSL error: {e}")
        except Exception as e:
            print(f"❌ General error: {e}")

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
