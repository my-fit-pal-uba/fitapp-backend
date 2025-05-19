import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import datetime
from flask import Flask
from flask_cors import CORS
from access_module.routes.login_controller import login_bp

DEFAULT_PORT = "8080"


class BackendApp:
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app, origins=["http://localhost:8081"], supports_credentials=True)
        self.app.register_blueprint(login_bp)
        self.register_routes()

    def register_routes(self):
        @self.app.route("/")
        def health_check():
            return str(datetime.now())

    def run(self):
        try:
            port_data = os.getenv("PORT", DEFAULT_PORT)
            port = int(port_data)
            self.app.run(host="0.0.0.0", port=port)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    backend_app = BackendApp()
    backend_app.run()
