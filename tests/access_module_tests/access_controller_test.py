import os
import sys
import unittest


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


class LoginControllerTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test01_login_success(self):
        pass


if __name__ == "__main__":
    unittest.main()
