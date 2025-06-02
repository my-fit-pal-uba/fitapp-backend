class Rol:

    def __init__(
        self, id: int, name: str, resource_key: str, description: str, icon: str
    ):
        self.id = id
        self.name = name
        self.resource_key = resource_key
        self.description = description
        self.icon = icon

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "icon": self.icon,
        }
