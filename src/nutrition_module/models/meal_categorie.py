class MealCategory:

    def __init__(self, id: int, description: str):
        self.id = id
        self.description = description

    def to_dict(self):
        return {"id": self.id, "description": self.description}
