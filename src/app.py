from flask import Flask
import os 

app = Flask(__name__)

DEFAULT_PORT = '8080'

@app.route('/')
def home():
    return "¡Hola, Docker con Flask!"

if __name__ == '__main__':
    try:
        port_data = os.getenv('PORT', DEFAULT_PORT)
        port = int(port_data)
        app.run(host='0.0.0.0', port=port_data)
    except Exception as e:
        print(f"Error: {e}")

    
