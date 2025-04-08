import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  #

from datetime import datetime
from flask import Flask
from flask_cors import CORS
import os
from src.routes.login_controller import login_bp

app = Flask(__name__)
CORS(app, origins=["http://localhost:8081"], supports_credentials=True)
app.register_blueprint(login_bp)

DEFAULT_PORT = "8080"


@app.route("/")
def health_check():
    return str(datetime.now())


if __name__ == "__main__":
    try:
        port_data = os.getenv("PORT", DEFAULT_PORT)
        port = int(port_data)
        app.run(host="0.0.0.0", port=port)
    except Exception as e:
        print(f"Error: {e}")
