import os
import sys
import unittest
from unittest.mock import MagicMock
from src.access_module.routes.login_controller import LoginController


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


class LoginControllerTestCase(unittest.TestCase):
    def setUp(self):
        # Mock del servicio
        self.mock_service = MagicMock()
        # Instancia del controller con el mock
        self.controller = LoginController(self.mock_service)

    def test01_login_success(self):
        self.mock_service.login("Prueba", "1").return_value = True
        result = self.controller.login("Prueba", "1")
        self.assertEqual(result.status_code, 200)
        self.assertTrue(result.json["result"])


if __name__ == "__main__":
    unittest.main()
