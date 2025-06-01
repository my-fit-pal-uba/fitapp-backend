from flask import Flask
import os
from flask_cors import CORS
from flasgger import Swagger  # type: ignore
from access_module.routes.login_controller import LoginController
from access_module.routes.user_controller import UserController
from access_module.repository.abstract_access_repository import AbstractAccessRepository
from access_module.repository.access_repository import AccessRepository
from access_module.services.login import Login
from access_module.services.abstract_login import AbstractAccessService
from access_module.routes.login_proxy import LoginProxy
from access_module.routes.user_proxy import UserProxy

from exercise_module.repository.abstract_exercise_repository import (
    AbstractExerciseRepository,
)
from exercise_module.repository.exercise_repository import ExerciseRepository
from exercise_module.services.abstract_exercise import AbstractExerciseService
from exercise_module.services.exercise import ExerciseService
from exercise_module.routes.exercise_controller import ExerciseController
from exercise_module.routes.exercise_proxy import ExerciseProxy
from profile_module.routes.profile_controller import ProfileController
from profile_module.routes.profile_proxy import ProfileProxy

DEFAULT_PORT = "8080"


class BackendApp:
    def __init__(self):
        self.app = Flask(__name__)
        Swagger(self.app)
        CORS(self.app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        self.register_healt_check()
        self.inyect_login_service()
        self.inject_user_service()
        self.inject_exercise_service()
        self.inyect_registrarion_service()

    def inyect_login_service(self):
        login_repository: AbstractAccessRepository = AccessRepository()
        login_service: AbstractAccessService = Login(login_repository)
        login_controller: LoginController = LoginController(login_service)
        login_proxy = LoginProxy(login_controller)
        self.app.register_blueprint(login_proxy.login_bp)

    def inject_user_service(self):
        user_repository: AbstractAccessRepository = AccessRepository()
        user_controller = UserController(user_repository)
        user_proxy = UserProxy(user_controller)
        self.app.register_blueprint(user_proxy.user_bp)

    def inject_exercise_service(self):
        exercise_repository: AbstractExerciseRepository = ExerciseRepository()
        exercise_service: AbstractExerciseService = ExerciseService(exercise_repository)
        exercise_controller: ExerciseController = ExerciseController(exercise_service)
        exercise_proxy = ExerciseProxy(exercise_controller)
        self.app.register_blueprint(exercise_proxy.exercise_bp)

    def inyect_registrarion_service(self):
        profile_controller = ProfileController()
        profile_proxy = ProfileProxy(profile_controller)
        self.app.register_blueprint(profile_proxy.profile_bp)

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
