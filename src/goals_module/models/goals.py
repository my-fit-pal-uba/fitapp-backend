from typing import Optional
from datetime import datetime


class Goals:
    """Clase que representa un objetivo"""

    def __init__(
        self,
        user_id: int,
        goal_value: float,
        registered_at: Optional[datetime] = None,
    ):
        self.user_id = user_id
        self.goal_value = goal_value
        self.registered_at = registered_at or datetime.now()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "goal_value": self.goal_value,
            "registered_at": self.registered_at.isoformat(),
        }
