import unittest
import random
import os
from packages.Player import Player

SAVE_FILE_LOCATION = "./data/"
SAVE_FILE_NAME = "data.bin"


class PlayerTester(unittest.TestCase):
    def backup_current_data(self):
        save_path = SAVE_FILE_LOCATION+SAVE_FILE_NAME
        os.system(f"cp {save_path} {save_path+"_bp"}")
        os.system(f"rm {save_path}")

    def restore_current_data(self):
        save_path = SAVE_FILE_LOCATION+SAVE_FILE_NAME
        os.system(f"cp {save_path+"_bp"} {save_path}")
        os.system(f"rm {save_path+"_bp"}")

    def test_can_create_file(self):
        save_path = SAVE_FILE_LOCATION+SAVE_FILE_NAME
        self.backup_current_data()

        self.assertFalse(os.path.exists(save_path))

        player = Player()
        player.save_acummulated_score()

        self.assertTrue(os.path.exists(save_path))
        self.restore_current_data()

    def test_save_load_acummulated_score(self):
        self.backup_current_data()

        player_mgr = Player()
        for _ in range(1000):
            random_score = random.randint(1, 100000)
            player_mgr.acummulated_score = random_score
            player_mgr.save_acummulated_score()
            player_mgr.acummulated_score = 0
            player_mgr.load_acummulated_score()
            self.assertEqual(player_mgr.acummulated_score, random_score)

        self.restore_current_data()


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
