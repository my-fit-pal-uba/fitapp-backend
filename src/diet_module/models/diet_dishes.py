class DietDishes:
    def __init__(
        self,
        id: int,
        dish_id: int,
        diet_id: int,
        meal_category_id: int,
        serving_size: float,
    ):
        self.id = id
        self.dish_id = dish_id
        self.diet_id = diet_id
        self.meal_category_id = meal_category_id
        self.serving_size = serving_size

    def to_dict(self):
        return {
            "id": self.id,
            "dish_id": self.dish_id,
            "diet_id": self.diet_id,
            "meal_category_id": self.meal_category_id,
            "serving_size": self.serving_size,
        }

    @classmethod
    def from_dict(cls, diet_dishes_dict: dict):
        return cls(
            id=diet_dishes_dict.get("id"),
            dish_id=diet_dishes_dict.get("dish_id"),
            diet_id=diet_dishes_dict.get("diet_id"),
            meal_category_id=diet_dishes_dict.get("meal_category_id"),
            serving_size=diet_dishes_dict.get("serving_size"),
        )

    def is_valid(self):
        conditions = [
            self.dish_id is not None and isinstance(self.dish_id, int),
            self.diet_id is not None and isinstance(self.diet_id, int),
            self.meal_category_id is not None
            and isinstance(self.meal_category_id, int),
            isinstance(self.serving_size, (int, float)) and self.serving_size > 0,
        ]
        return all(conditions)
