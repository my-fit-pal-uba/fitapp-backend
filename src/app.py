from flask import Flask
import os
from flask_cors import CORS
from flasgger import Swagger  # type: ignore
from access_module.routes.login_controller import LoginController
from access_module.repository.abstract_access_repository import AbstractAccessRepository
from access_module.repository.access_repository import AccessRepository
from access_module.services.login import Login
from access_module.services.abstract_login import AbstractAccessService
from access_module.routes.login_proxy import LoginProxy

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
from profile_module.repository.profile_repository import ProfileRepository
from profile_module.services.abstract_profile_service import AbstractProfileService
from profile_module.services.profile import ProfileService
from history_module.repository.abstract_history_repository import (
    AbstractHistoryRepository,
)
from history_module.repository.history_repository import HistoryRepository
from history_module.routes.history_controller import HistoryController
from history_module.routes.history_proxy import HistoryProxy
from history_module.services.abstract_history_service import AbstractHistoryService
from history_module.services.history import HistoryService
from diet_module.routes.diet_controller import DietController
from diet_module.routes.diet_proxy import DietProxy
from nutrition_module.repository.abstract_nutrition_repository import (
    AbstractNutritionRepository,
)
from nutrition_module.routes.nutrition_controller import NutritionController
from nutrition_module.routes.nutrition_proxy import NutritionProxy
from nutrition_module.service.abstract_nutrition_service import (
    AbstractNutritionService,
)
from nutrition_module.service.nutrition import NutritionService
from nutrition_module.repository.nutrition_repository import NutritionRepository
from diet_module.service.abstract_service import AbstractDietService
from diet_module.service.diet_service import DietService
from diet_module.repository.diet_repository import DietRepository

from goals_module.repository.abstract_goals_repository import (
    AbstractGoalsRepository,
)
from goals_module.repository.goals_repository import GoalsRepository
from goals_module.services.abstract_goals_service import AbstractGoalsService
from goals_module.services.goals_service import GoalsService
from goals_module.routes.goals_controller import GoalsController
from goals_module.routes.goals_proxy import GoalsProxy

from routine_module.repository.abstract_routine_repository import (
    AbstractRoutineRepository,
)
from routine_module.repository.routine_repository import RoutineRepository
from routine_module.services.abstract_routine_service import AbstractRoutineService
from routine_module.services.routine_service import RoutineService
from routine_module.routes.routine_controller import RoutineController
from routine_module.routes.routine_proxy import RoutineProxy

from trainer_module.repository.abstract_trainer_repository import (
    AbstractTrainerRepository,
)
from trainer_module.repository.trainer_repository import TrainerRepository
from trainer_module.services.abstract_trainer_service import AbstractTrainerService
from trainer_module.services.trainer_service import TrainerService
from trainer_module.routes.trainer_controller import TrainerController
from trainer_module.routes.trainer_proxy import TrainerProxy


DEFAULT_PORT = "8080"


class BackendApp:
    def __init__(self):
        self.app = Flask(__name__)
        Swagger(self.app)
        CORS(self.app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
        self.register_healt_check()
        self.inyect_login_service()
        self.inject_exercise_service()
        self.inyect_registrarion_service()
        self.inyect_history_service()
        self.inyect_diet_service()
        self.inyect_nutrition_service()
        self.inject_routine_service()
        self.inject_goals_service()
        self.inject_trainer_service()

    def inyect_login_service(self):
        login_repository: AbstractAccessRepository = AccessRepository()
        login_service: AbstractAccessService = Login(login_repository)
        login_controller: LoginController = LoginController(login_service)
        login_proxy = LoginProxy(login_controller)
        self.app.register_blueprint(login_proxy.login_bp)

    def inject_exercise_service(self):
        exercise_repository: AbstractExerciseRepository = ExerciseRepository()
        exercise_service: AbstractExerciseService = ExerciseService(exercise_repository)
        exercise_controller: ExerciseController = ExerciseController(exercise_service)
        exercise_proxy = ExerciseProxy(exercise_controller)
        self.app.register_blueprint(exercise_proxy.exercise_bp)

    def inyect_registrarion_service(self):
        profile_respository: AbstractProfileService = ProfileRepository()
        profile_service: AbstractProfileService = ProfileService(profile_respository)
        profile_controller = ProfileController(profile_service)
        profile_proxy = ProfileProxy(profile_controller)
        self.app.register_blueprint(profile_proxy.profile_bp)

    def inyect_history_service(self):
        history_repository: AbstractHistoryRepository = HistoryRepository()
        history_service: AbstractHistoryService = HistoryService(history_repository)
        history_controller: HistoryController = HistoryController(history_service)
        history_proxy = HistoryProxy(history_controller)
        self.app.register_blueprint(history_proxy.history_bp)

    def inyect_nutrition_service(self):
        nutrition_repository: AbstractNutritionRepository = NutritionRepository()
        nutrition_service: AbstractNutritionService = NutritionService(
            nutrition_repository
        )
        nutrition_controller: NutritionController = NutritionController(
            nutrition_service
        )
        nutrition_proxy = NutritionProxy(nutrition_controller)
        self.app.register_blueprint(nutrition_proxy.nutrition_bp)

    def inyect_diet_service(self):
        diet_repository: AbstractDietService = DietRepository()
        diet_service: AbstractDietService = DietService(diet_repository)
        diet_controller: DietController = DietController(diet_service)
        diet_proxy = DietProxy(diet_controller)
        self.app.register_blueprint(diet_proxy.diet_bp)

    def inject_routine_service(self):
        routine_repository: AbstractRoutineRepository = RoutineRepository()
        routine_service: AbstractRoutineService = RoutineService(routine_repository)
        routine_controller: RoutineController = RoutineController(routine_service)
        routine_proxy = RoutineProxy(routine_controller)
        self.app.register_blueprint(routine_proxy.routine_bp)

    def inject_goals_service(self):
        goals_repository: AbstractGoalsRepository = GoalsRepository()
        goals_service: AbstractGoalsService = GoalsService(goals_repository)
        goals_controller: GoalsController = GoalsController(goals_service)
        goals_proxy = GoalsProxy(goals_controller)
        self.app.register_blueprint(goals_proxy.goals_bp)

    def inject_trainer_service(self):
        trainer_repository: AbstractTrainerRepository = TrainerRepository()
        trainer_service: AbstractTrainerService = TrainerService(trainer_repository)
        trainer_controller: TrainerController = TrainerController(trainer_service)
        trainer_proxy = TrainerProxy(trainer_controller)
        self.app.register_blueprint(trainer_proxy.trainer_bp)

    def register_healt_check(self):
        @self.app.route("/")
        def health_check():
            from datetime import datetime

            return str(datetime.now())

    def run(self):
        try:
            port_data = os.getenv("PORT", DEFAULT_PORT)
            port = int(port_data)
            self.app.run(host="0.0.0.0", port=port, debug=True)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    BackendApp().run()
