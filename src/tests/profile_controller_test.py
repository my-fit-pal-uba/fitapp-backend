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
        self.mock_service.register_daily_weight.return_value = True
        result, data, code = self.controller.register_daily_weight(1, 70.5)
        self.assertTrue(result)
        self.assertEqual(data, {"message": "Daily weight registered successfully"})
        self.assertEqual(code, 200)
        self.mock_service.register_daily_weight.assert_called_once_with(1, 70.5)

    def test_register_daily_weight_missing_params(self):
        result, data, code = self.controller.register_daily_weight(0, 0)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "User ID and weight are required"})
        self.assertEqual(code, 400)

    def test_register_daily_weight_fail(self):
        self.mock_service.register_daily_weight.return_value = False
        result, data, code = self.controller.register_daily_weight(1, 70.5)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Failed to register daily weight"})
        self.assertEqual(code, 500)

    def test_register_daily_calories_success(self):
        self.mock_service.register_daily_calories.return_value = True
        result, data, code = self.controller.register_daily_calories(1, 2000)
        self.assertTrue(result)
        self.assertEqual(data, {"message": "Daily calories registered successfully"})
        self.assertEqual(code, 200)
        self.mock_service.register_daily_calories.assert_called_once_with(1, 2000)

    def test_register_daily_calories_missing_params(self):
        result, data, code = self.controller.register_daily_calories(0, 0)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "User ID and calories are required"})
        self.assertEqual(code, 400)

    def test_register_daily_calories_fail(self):
        self.mock_service.register_daily_calories.return_value = False
        result, data, code = self.controller.register_daily_calories(1, 2000)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Failed to register daily calories"})
        self.assertEqual(code, 500)

    def test_save_profile_success(self):
        mock_profile = MagicMock()
        mock_profile.user_id = 1
        self.mock_service.save_profile.return_value = True
        result, data, code = self.controller.save_profile(mock_profile)
        self.assertTrue(result)
        self.assertEqual(data, {"message": "Profile saved successfully"})
        self.assertEqual(code, 200)
        self.mock_service.save_profile.assert_called_once_with(mock_profile)

    def test_save_profile_missing_profile(self):
        result, data, code = self.controller.save_profile(None)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "User ID and profile data are required"})
        self.assertEqual(code, 400)

    def test_save_profile_missing_user_id(self):
        mock_profile = MagicMock()
        mock_profile.user_id = None
        result, data, code = self.controller.save_profile(mock_profile)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "User ID and profile data are required"})
        self.assertEqual(code, 400)

    def test_save_profile_fail(self):
        mock_profile = MagicMock()
        mock_profile.user_id = 1
        self.mock_service.save_profile.return_value = False
        result, data, code = self.controller.save_profile(mock_profile)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Failed to save profile"})
        self.assertEqual(code, 500)

    def test_get_profile_success(self):
        mock_profile = MagicMock()
        mock_profile.to_dict.return_value = {"user_id": 1, "name": "Test"}
        self.mock_service.get_profile.return_value = mock_profile
        result, data, code = self.controller.get_profile(1)
        self.assertTrue(result)
        self.assertEqual(data, {"user_id": 1, "name": "Test"})
        self.assertEqual(code, 200)
        self.mock_service.get_profile.assert_called_once_with(1)

    def test_get_profile_missing_user_id(self):
        result, data, code = self.controller.get_profile(0)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "User ID is required"})
        self.assertEqual(code, 400)

    def test_get_profile_not_found(self):
        self.mock_service.get_profile.return_value = None
        result, data, code = self.controller.get_profile(1)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Profile not found"})
        self.assertEqual(code, 404)

    def test_get_user_rols(self):
        self.mock_service.get_user_rols.return_value = ["admin", "user"]
        result, data, code = self.controller.get_user_rols()
        self.assertTrue(result)
        self.assertEqual(data, {"rols": ["admin", "user"]})
        self.assertEqual(code, 200)
        self.mock_service.get_user_rols.assert_called_once_with()

    def test_register_user_rol_success(self):
        self.mock_service.register_user_rol.return_value = True
        result, data, code = self.controller.register_user_rol(1, 2)
        self.assertTrue(result)
        self.assertEqual(data, {"message": "User role registered successfully"})
        self.assertEqual(code, 200)
        self.mock_service.register_user_rol.assert_called_once_with(1, 2)

    def test_register_user_rol_missing_params(self):
        result, data, code = self.controller.register_user_rol(0, 0)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "User ID and role are required"})
        self.assertEqual(code, 400)

    def test_register_user_rol_result_none(self):
        self.mock_service.register_user_rol.return_value = None
        result, data, code = self.controller.register_user_rol(1, 2)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "Failed to register user role"})
        self.assertEqual(code, 500)

    def test_register_user_rol_result_false(self):
        self.mock_service.register_user_rol.return_value = False
        result, data, code = self.controller.register_user_rol(1, 2)
        self.assertFalse(result)
        self.assertEqual(data, {"error": "An error has ocurred"})
        self.assertEqual(code, 400)


if __name__ == "__main__":
    unittest.main()
