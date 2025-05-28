from flask import Flask
import os
from flask_cors import CORS
from flasgger import Swagger  # type: ignore
from access_module.routes.login_controller import LoginController
from access_module.repository.access_repository import AccessRepository
from access_module.services.login import Login
from access_module.services.abstract_login import AbstractAccessService
from access_module.repository.abstract_access_repository import AbstractAccessRepository
from access_module.routes.login_proxy import LoginProxy

DEFAULT_PORT = "8080"


class BackendApp:
    def __init__(self):
        self.app = Flask(__name__)
        Swagger(self.app)
        CORS(self.app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        self.register_healt_check()
        self.inyect_login_service()

    def inyect_login_service(self):
        login_repository: AbstractAccessRepository = AccessRepository()
        login_service: AbstractAccessService = Login(login_repository)
        login_controller: LoginController = LoginController(login_service)
        login_proxy = LoginProxy(login_controller)
        self.app.register_blueprint(login_proxy.login_bp)

    def register_healt_check(self):
        @self.app.route("/")
        def health_check():
            from datetime import datetime

            return str(datetime.now())

    def run(self):
        try:
            port_data = os.getenv("PORT", DEFAULT_PORT)
            port = int(port_data)
            self.app.run(host="0.0.0.0", port=port)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    BackendApp().run()
