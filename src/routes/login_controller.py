from flask import Blueprint
from services.login import Login

login_bp = Blueprint('login', __name__, url_prefix='/login')

login_service = Login() 

@login_bp.route('/')
def login():
    return login_service.say_hello()