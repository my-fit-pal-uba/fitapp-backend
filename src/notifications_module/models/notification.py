class Notification:
    def __init__(self, id: int, description: str, date: str):
        self.id = id
        self.description = description
        self.date = date

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "description": self.description,
            "date": self.date,
            "read": self.read,
        }
