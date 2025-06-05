from typing import Optional

class Routine: 
    """Clase que repersenta una rutina del sistema."""

    def __init__(
        self,
        routine_id: Optional[int] = None
    ):
        self.routine_id = routine_id

    def to_dict(self):
        return {
            "routine_id": self.routine_id
        }