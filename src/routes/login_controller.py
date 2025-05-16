from flask import Blueprint
from src.services.login import Login

login_bp = Blueprint("login", __name__, url_prefix="/access")

login_service = Login()


@login_bp.route("/login")
def login():
    return login_service.say_hello()


@login_bp.route("/signin")
def sign_in():
    try:
        return login_service.sign_in()
    except Exception as e:
        print(e)
        return ""

@login_bp.route("/users")
def get_users():
    try:
        print("Pase por aca")
        return login_service.get_users()
    except Exception as e:
        return []
    
