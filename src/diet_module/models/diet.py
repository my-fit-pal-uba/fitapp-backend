class Diet:
    def __init__(
        self,
        id: int,
        name: str,
        observation: str,
    ):
        self.id = id
        self.name = name
        self.observation = observation

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "observation": self.observation,
        }

    @classmethod
    def from_dict(cls, diet_dict: dict):
        return cls(
            id=diet_dict.get("id"),
            name=diet_dict.get("name"),
            observation=diet_dict.get("observation"),
        )

    def is_valid(self):
        conditions = [
            isinstance(self.name, str) and len(self.name) > 0,
            isinstance(self.observation, str),
        ]
        return all(conditions)
