class dish:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        calories: float,
        proteins: float,
        carbohydrates: float,
        fats: float,
        weight: float,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.calories = calories
        self.proteins = proteins
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.weight = weight

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "calories": self.calories,
            "proteins": self.proteins,
            "carbohydrates": self.carbohydrates,
            "fats": self.fats,
            "weight": self.weight,
        }
