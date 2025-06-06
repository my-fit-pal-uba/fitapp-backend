class dish:
    def __init__(
        self,
        name: str,
        calories: float,
        proteins: float,
        carbohydrates: float,
        fats: float,
        ingredients: list,
    ):
        self.name = name
        self.calories = calories
        self.proteins = proteins
        self.carbohydrates = carbohydrates
        self.fats = fats
        self.ingredients = ingredients
        self.name = name
        self.calories = calories

    def to_dict(self):
        return {
            "name": self.name,
            "calories": self.calories,
            "ingredients": self.ingredients,
        }
