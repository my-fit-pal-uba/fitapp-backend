from typing import Optional

class Exercise:
    """Clase que repersenta un ejercicio del sistema."""

    def __init__(
            self,
            name: str,
            description: str,
            muscular_group: str,
            type: str,
            place: str,
            photo_guide: Optional[str] = None,
            video_guide: Optional[str] = None,
            exercise_id: Optional[int] = None,       
    ):
        self.exercise_id = exercise_id
        self.name = name
        self.description = description
        self.muscular_group = muscular_group
        self.type = type
        self.place = place
        self.photo_guide = photo_guide
        self.video_guide = video_guide

    def to_dict(self):
        return {
            "exercise_id": self.exercise_id,
            "name": self.name,
            "description": self.description,
            "muscular_group": self.muscular_group,
            "type": self.type,
            "place": self.place,
            "photo_guide": self.photo_guide,
            "video_guide": self.video_guide,
        }