from typing import Optional
from datetime import datetime


class User:
    """Clase que representa un usuario del sistema."""

    def __init__(
        self,
        email: str,
        password_hash: str,
        is_active: bool = True,
        is_superuser: bool = False,
        first_name: Optional[str] = None,
        last_login: Optional[datetime] = None,
        last_name: Optional[str] = None,
        user_id: Optional[int] = None,
        username: Optional[str] = None,
    ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.is_superuser = is_superuser
        self.last_login = last_login
        self.password_hash = password_hash

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "last_login": self.last_login.isoformat() if self.last_login else None,
        }
