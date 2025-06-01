import unittest
from unittest.mock import MagicMock
from profile_module.routes.profile_controller import ProfileController


class TestProfileController(unittest.TestCase):
    def setUp(self):
        self.mock_service = MagicMock()
        self.controller = ProfileController(self.mock_service)

    def test_register_rol_success(self):
        self.mock_service.register_rol.return_value = True
        result, data, code = self.controller.register_rol("admin", 1)
        self.assertTrue(result)
        self.assertEqual(data, {"message": "Role registered successfully"})
        self.assertEqual(code, 200)
        self.mock_service.register_rol.assert_called_once_with("admin", 1)

    def test_register_rol_missing_params(self):
        result, data, code = self.controller.register_rol("", 0)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Role and user ID are required"})
        self.assertEqual(code, 400)

    def test_register_rol_fail(self):
        self.mock_service.register_rol.return_value = False
        result, data, code = self.controller.register_rol("admin", 1)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Failed to register role"})
        self.assertEqual(code, 500)

    def test_register_daily_weight_success(self):
        self.mock_service.post_daily_weight.return_value = True
        result, data, code = self.controller.register_daily_weight(1, 70.5)
        self.assertTrue(result)
        self.assertEqual(data, {"message": "Daily weight registered successfully"})
        self.assertEqual(code, 200)
        self.mock_service.post_daily_weight.assert_called_once_with(1, 70.5)

    def test_register_daily_weight_missing_params(self):
        result, data, code = self.controller.register_daily_weight(0, 0)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "User ID and weight are required"})
        self.assertEqual(code, 400)

    def test_register_daily_weight_fail(self):
        self.mock_service.post_daily_weight.return_value = False
        result, data, code = self.controller.register_daily_weight(1, 70.5)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Failed to register daily weight"})
        self.assertEqual(code, 500)

    def test_register_daily_calories_success(self):
        self.mock_service.post_daily_calories.return_value = True
        result, data, code = self.controller.register_daily_calories(1, 2000)
        self.assertTrue(result)
        self.assertEqual(data, {"message": "Daily calories registered successfully"})
        self.assertEqual(code, 200)
        self.mock_service.post_daily_calories.assert_called_once_with(1, 2000)

    def test_register_daily_calories_missing_params(self):
        result, data, code = self.controller.register_daily_calories(0, 0)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "User ID and calories are required"})
        self.assertEqual(code, 400)

    def test_register_daily_calories_fail(self):
        self.mock_service.post_daily_calories.return_value = False
        result, data, code = self.controller.register_daily_calories(1, 2000)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Failed to register daily calories"})
        self.assertEqual(code, 500)


if __name__ == "__main__":
    unittest.main()
