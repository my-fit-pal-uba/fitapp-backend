import unittest
from unittest.mock import MagicMock
from profile_module.services.profile import ProfileService
from models.profile import Profile


class TestProfileService(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.service = ProfileService(self.mock_repo)

    def test_register_rol(self):
        self.mock_repo.register_rol.return_value = True
        result = self.service.register_rol("admin", 1)
        self.assertEqual(result, True)
        self.mock_repo.register_rol.assert_called_once_with("admin", 1)

    def test_register_daily_weight(self):
        self.mock_repo.register_daily_weight.return_value = True
        result = self.service.register_daily_weight(1, 70.5)
        self.assertEqual(result, True)
        self.mock_repo.register_daily_weight.assert_called_once_with(1, 70.5)

    def test_register_daily_calories(self):
        self.mock_repo.register_daily_calories.return_value = True
        result = self.service.register_daily_calories(1, 2000)
        self.assertEqual(result, True)
        self.mock_repo.register_daily_calories.assert_called_once_with(1, 2000)

    def test_get_profile(self):
        mock_profile = MagicMock(spec=Profile)
        self.mock_repo.get_profile.return_value = mock_profile
        result = self.service.get_profile(1)
        self.assertEqual(result, mock_profile)
        self.mock_repo.get_profile.assert_called_once_with(1)

    def test_save_profile(self):
        mock_profile = MagicMock(spec=Profile)
        self.mock_repo.save_profile.return_value = True
        result = self.service.save_profile(mock_profile)
        self.assertTrue(result)
        self.mock_repo.save_profile.assert_called_once_with(mock_profile)

    def test_get_user_rols(self):
        self.mock_repo.get_user_rols.return_value = ["admin", "user"]
        result = self.service.get_user_rols()
        self.assertEqual(result, ["admin", "user"])
        self.mock_repo.get_user_rols.assert_called_once_with()

    # def test_post_user_rol_success(self):
    #     self.mock_repo.post_user_rol.return_value = ("ok",)
    #     result = self.service.post_user_rol(1, 2)
    #     self.assertEqual(result, ("ok",))
    #     self.mock_repo.post_user_rol.assert_called_once_with(1, 2)

    # def test_post_user_rol_exception(self):
    #     self.mock_repo.post_user_rol.side_effect = Exception("DB error")
    #     result = self.service.post_user_rol(1, 2)
    #     self.assertIsNone(result)
    #     self.mock_repo.post_user_rol.assert_called_once_with(1, 2)


if __name__ == "__main__":
    unittest.main()
