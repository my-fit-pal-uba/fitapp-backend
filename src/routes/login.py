from flask import Blueprint

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/')
def login():
    return "¡Hola desde la página principal!"
