from flask import Flask
from flask_cors import CORS

from access_module.routes.login_controller import LoginController
from access_module.repository.access_repository import AccessRepository
from access_module.services.login import Login
from access_module.services.abstract_login import AbstractAccessService
from access_module.repository.abstract_access_repository import AbstractAccessRepository

DEFAULT_PORT = "8080"


class BackendApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, origins=["http://localhost:8081"], supports_credentials=True)
        # self.app.register_blueprint(container.login_blueprint())
        self.register_routes()

    def inyect_login_service(self):
        login_repository: AbstractAccessRepository = AccessRepository()
        login_service: AbstractAccessService = Login(login_repository)
        login_controller: LoginController = LoginController(login_service)
        self.app.register_blueprint(login_controller.login_bp)

        # login_repository: AbstractLoginRepository = AccessRepository()

    def register_routes(self):
        @self.app.route("/")
        def health_check():
            from datetime import datetime

            return str(datetime.now())

    def run(self):
        import os

        try:
            port_data = os.getenv("PORT", DEFAULT_PORT)
            port = int(port_data)
            self.app.run(host="0.0.0.0", port=port)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    BackendApp().run()
