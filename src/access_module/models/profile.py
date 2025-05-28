from typing import Optional
from datetime import datetime


class Profile:
    """Clase que representa un usuario del sistema."""

    def __init__(
        self,
        user_id: Optional[int] = None,
        age: Optional[int] = None,
        height: Optional[int] = None,
        gender: Optional[str] = None,
    ):
        self.user_id = user_id
        self.age = age
        self.height = height
        self.gender = gender

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "age": self.age,
            "height": self.height,
            "gender": self.gender,
        }