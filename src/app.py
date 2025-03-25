from datetime import datetime
from flask import Flask
import os 
from routes.login_controller import login_bp

app = Flask(__name__)
app.register_blueprint(login_bp)

DEFAULT_PORT = '8080'

@app.route('/')
def health_check():
    return str(datetime.now())

if __name__ == '__main__':
    try:
        port_data = os.getenv('PORT', DEFAULT_PORT)
        port = int(port_data)
        app.run(host='0.0.0.0', port=port_data)
    except Exception as e:
        print(f"Error: {e}")

    
