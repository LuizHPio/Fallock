from packages.Vector2 import Vector2
import unittest


class Vector2Tester(unittest.TestCase):

    def test_add_positive(self):
        posVector = Vector2(2, 2)
        posVector.x += 1
        posVector.y += 2

        self.assertEqual(posVector.x, 3)
        self.assertEqual(posVector.y, 4)

    def test_add_negative(self):
        posVector = Vector2(2, 2)
        posVector.x += -4
        posVector.y += -7

        self.assertEqual(posVector.x, -2)
        self.assertEqual(posVector.y, -5)


if __name__ == "__main__":
    unittest.main()
