from typing import Optional, List
from exercise_module.models.exercise import Exercise


class Routine:
    """Clase que representa una rutina del sistema."""

    def __init__(
        self,
        name: str,
        muscular_group: str,
        description: str,
        series: int,
        exercises: List[Exercise],
        routine_id: Optional[int] = None,
    ):
        self.routine_id = routine_id
        self.name = name
        self.muscular_group = muscular_group
        self.description = description
        self.series = series
        self.exercises = exercises

    def to_dict(self):
        return {
            "routine_id": self.routine_id,
            "name": self.name,
            "muscular_group": self.muscular_group,
            "description": self.description,
            "series": self.series,
            "exercises": [e.to_dict() for e in self.exercises],
        }
