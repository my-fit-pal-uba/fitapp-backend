class dish:
    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        calories: float,
        proteins: float,
        carbs: float,
        fats: float,
        weight: float,
        id_dish_category: list[int],
    ):
        self.id = id
        self.name = name
        self.description = description
        self.calories = calories
        self.proteins = proteins
        self.carbs = carbs
        self.fats = fats
        self.weight = weight
        self.id_dish_category = id_dish_category

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "calories": self.calories,
            "proteins": self.proteins,
            "carbs": self.carbs,
            "fats": self.fats,
            "weight": self.weight,
            "id_dish_category": self.id_dish_category,
        }

    @classmethod
    def from_dict(cls, dish_dict: dict):
        return cls(
            id=dish_dict.get("id"),
            name=dish_dict.get("name"),
            description=dish_dict.get("description"),
            calories=dish_dict.get("calories"),
            proteins=dish_dict.get("proteins"),
            carbs=dish_dict.get("carbohydrates"),
            fats=dish_dict.get("fats"),
            weight=dish_dict.get("weight"),
            id_dish_category=dish_dict.get("id_dish_category"),
        )

    def is_valid(self):
        conditions = [
            len(self.name) > 0,
            isinstance(self.description, str),
            self.calories >= 0,
            self.proteins >= 0,
            self.carbs >= 0,
            self.fats >= 0,
            self.weight > 0,
            self.id_dish_category is not None and self.id_dish_category != [],
        ]
        return all(conditions)
