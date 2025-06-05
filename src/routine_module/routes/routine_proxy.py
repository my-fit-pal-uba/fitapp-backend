from flask import Blueprint, request

from routine_module.routes.routine_controller import RoutineController
from models.response import ResponseInfo

class RoutineProxy:
    def __init__(self, routine_controller: RoutineController):
        self.routine_controller = routine_controller
        self.routine_bp = Blueprint("routine", __name__, url_prefix="/routines")
        self.register_routes()

    def register_routes(self):
        """
        """