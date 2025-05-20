import os
import sys
import unittest


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import MagicMock
from access_module.routes.login_controller import LoginController
from access_module.exceptions.non_existing_user import NonExistingUser
from access_module.exceptions.invalid_password import InvalidUserPassword


class LoginControllerTest(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        self.controller = LoginController(self.mock_service)

    def test_login_success(self):
        self.mock_service.login.return_value = True
        result, msg, code = self.controller.login("test@mail.com", "1234")
        self.assertTrue(result)
        self.assertEqual(msg, "Login successful")
        self.assertEqual(code, 200)
        self.mock_service.login.assert_called_once_with("test@mail.com", "1234")

    def test_login_missing_params(self):
        result, msg, code = self.controller.login("", "")
        self.assertFalse(result)
        self.assertEqual(msg, "Email and password are required")
        self.assertEqual(code, 400)

    def test_login_non_existing_user(self):
        self.mock_service.login.side_effect = NonExistingUser("test@mail.com")
        result, msg, code = self.controller.login("test@mail.com", "1234")
        self.assertFalse(result)
        self.assertEqual(msg, "User does not exist")
        self.assertEqual(code, 404)

    def test_login_invalid_password(self):
        self.mock_service.login.side_effect = InvalidUserPassword("test@mail.com")
        result, msg, code = self.controller.login("test@mail.com", "wrong")
        self.assertFalse(result)
        self.assertEqual(msg, "Invalid password")
        self.assertEqual(code, 404)


if __name__ == "__main__":
    unittest.main()
