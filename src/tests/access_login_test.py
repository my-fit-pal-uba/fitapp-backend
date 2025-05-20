import os
import sys
import unittest


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock
from access_module.services.login import Login
from access_module.models.user import User
from access_module.exceptions.non_existing_user import NonExistingUser
from access_module.exceptions.invalid_password import InvalidUserPassword


class LoginServiceTest(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.login_service = Login(self.mock_repo)
        self.user = User(
            user_id=1,
            username="testuser",
            email="test@mail.com",
            first_name="Test",
            last_name="User",
            is_active=True,
            is_superuser=False,
            last_login=None,
            password_hash="1234",
        )

    def test_login_success(self):
        self.mock_repo.get_user_by_email.return_value = self.user
        result = self.login_service.login("test@mail.com", "1234")
        self.assertTrue(result)
        self.mock_repo.get_user_by_email.assert_called_once_with("test@mail.com")

    def test_login_non_existing_user(self):
        self.mock_repo.get_user_by_email.return_value = None
        with self.assertRaises(NonExistingUser):
            self.login_service.login("notfound@mail.com", "any")

    def test_login_invalid_password(self):
        self.user.password_hash = "wrong"
        self.mock_repo.get_user_by_email.return_value = self.user
        with self.assertRaises(InvalidUserPassword):
            self.login_service.login("test@mail.com", "1234")


if __name__ == "__main__":
    unittest.main()
