class DishConsumption:
    def __init__(self, dish_id: int, user_id: int, quantity: float):
        self.dish_id = dish_id
        self.user_id = user_id
        self.quantity = quantity

    def to_dict(self):
        return {
            "dish_id": self.dish_id,
            "user_id": self.user_id,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            dish_id=data.get("dish_id"),
            user_id=data.get("user_id"),
            quantity=data.get("weight"),
        )

    def is_valid(self):
        if not isinstance(self.dish_id, int) or self.dish_id <= 0:
            return False
        if not isinstance(self.user_id, int) or self.user_id <= 0:
            return False
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            return False
        return True
