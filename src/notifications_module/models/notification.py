class Notification:
    def __init__(self, id: int, description: str, date: str):
        self.id = id
        self.description = description
        self.date = date

    def to_dict(self):
        return {
            "id": self.id,
            "description": self.description,
            "date": self.date,
        }

    def from_dict(data: dict):
        return Notification(
            id=data.get("id"),
            description=data.get("description"),
            date=data.get("date"),
        )
