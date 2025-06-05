from typing import Optional
from datetime import datetime


class Serie:
    """Clase que repersenta una serie realizada."""

    def __init__(
        self,
        user_id: int,
        exercise_id: int,
        repetitions: int,
        weight: float = 0.0,
        created_at: Optional[datetime] = None,
    ):
        self.user_id = user_id
        self.exercise_id = exercise_id
        self.repetitions = repetitions
        self.weight = weight
        self.created_at = created_at

    def to_dict(self):
        data = {
            "user_id": self.user_id,
            "exercise_id": self.exercise_id,
            "repetitions": self.repetitions,
            "weight": self.weight,
        }
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()
        return data
