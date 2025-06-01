import unittest
from unittest.mock import MagicMock
from profile_module.services.profile import ProfileService


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


if __name__ == "__main__":
    unittest.main()
