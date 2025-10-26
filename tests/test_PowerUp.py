import unittest
from packages.PowerUp import PowerUp


class PowerUpTester(unittest.TestCase):

    def test_name_gets_assigned(self):
        for _ in range(100):
            pu = PowerUp()
            self.assertIsInstance(pu.name, str)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
