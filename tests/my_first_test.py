import sys
import os
import unittest


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class FirstTest(unittest.TestCase):
    """setup"""

    def setUp(self):
        # self.bag = Bag()
        # self.book_item = "book"
        # self.knife_item = "knife"
        pass

    """tests"""

    def test01_bag_is_empty(self):
        self.assertTrue(True)
