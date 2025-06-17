class Notification:
    def __init__(self, id: int, description: str, date: str, user_id: int = 0):
        self.id = id
        self.description = description
        self.date = date
        self.user_id = user_id

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
            user_id=data.get("user_id", 0),
        )
