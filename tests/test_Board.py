import unittest
from packages.Board import Board
from packages.Block import Block
from packages.Vector2 import Vector2
from packages.Piece import Piece
from packages.Player import Player
from packages.PowerUp import PowerUp


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        self.player_manager: Player = Player()
        self.board: Board = Board(
            width=9, height=20, player_manager=self.player_manager)

    def test_initialization(self) -> None:
        self.assertEqual(self.board.width, 9)
        self.assertEqual(self.board.height, 20)
        self.assertEqual(len(self.board.grid), 9)
        self.assertEqual(len(self.board.grid[0]), 20)
        self.assertIsNone(self.board.grid[0][0])
        self.assertIsNotNone(self.board.player_piece)
        self.assertEqual(self.board.player_piece.origin, Vector2(4, 0))
        self.assertFalse(self.board.is_animating)

    def test_has_collided_with_floor(self) -> None:
        self.board.player_piece = Piece(Vector2(0, 0), "PYRAMID")
        self.board.player_piece.origin = Vector2(
            5, 18)
        self.assertTrue(self.board.has_collided(self.board.player_piece))

    def test_has_collided_with_block(self) -> None:
        self.board.player_piece = Piece(Vector2(5, 8), "PYRAMID")
        self.board.grid[5][10] = Block()
        self.assertTrue(self.board.has_collided(self.board.player_piece))

    def test_no_collision(self) -> None:
        self.board.player_piece.origin = Vector2(5, 5)
        self.assertFalse(self.board.has_collided(self.board.player_piece))

    def test_block_collapse(self) -> None:

        for x in range(self.board.width):
            self.board.grid[x][self.board.height-1] = Block()

        self.board.grid[4][self.board.height-2] = Block()

        self.board.score_line()
        for _ in range(10):
            self.board.physics_logic()

        self.assertIsInstance(self.board.grid[4][19], Block)

    def test_petrify_piece(self) -> None:
        self.board.player_piece = Piece(Vector2(0, 0), "PYRAMID")
        piece_to_petrify: Piece = self.board.player_piece
        piece_to_petrify.origin = Vector2(5, 10)

        self.board.petrify_piece(piece_to_petrify)

        self.assertIsInstance(self.board.grid[5][10], Block)  # origin
        self.assertIsInstance(self.board.grid[4][11], Block)  # left part
        self.assertIsInstance(self.board.grid[6][11], Block)  # right part
        self.assertIsInstance(self.board.grid[5][11], Block)  # bottom part

        self.assertNotEqual(self.board.player_piece, piece_to_petrify)
        self.assertEqual(self.board.player_piece.origin, Vector2(4, 0))

    def test_movement(self) -> None:
        initial_x: int = self.board.player_piece.origin.x

        self.board.movement("RIGHT")
        self.assertEqual(self.board.player_piece.origin.x, initial_x + 1)

        self.board.movement("LEFT")
        self.assertEqual(self.board.player_piece.origin.x, initial_x)

    def test_physics_logic_gravity(self) -> None:
        initial_y: int = self.board.player_piece.origin.y
        self.board.physics_logic()
        self.assertEqual(self.board.player_piece.origin.y, initial_y + 1)

    def test_physics_logic_collision(self) -> None:
        self.board.player_piece = Piece(Vector2(0, 0), 'PYRAMID')
        self.board.player_piece.origin = Vector2(
            5, 18)
        self.board.physics_logic()
        self.assertIsInstance(self.board.grid[5][18], Block)
        self.assertIsInstance(self.board.grid[5][19], Block)
        self.assertEqual(self.board.player_piece.origin.y, 0)

    def test_explode_bomb_clears_spaces(self) -> None:
        self.board.player_manager.power_up = PowerUp()

        self.board.player_manager.power_up.is_active = True
        self.board.player_manager.power_up.name = "BOMB"

        check_vectors = [Vector2(5, 2),
                         Vector2(4, 3), Vector2(5, 3), Vector2(6, 3),
                         Vector2(3, 4), Vector2(4, 4), Vector2(
                             6, 4), Vector2(7, 4),
                         Vector2(4, 5), Vector2(5, 5), Vector2(6, 5),
                         Vector2(5, 6)]

        for check_vector in check_vectors:
            self.board.grid[check_vector.x][check_vector.y] = Block()

        self.board.generate_piece("BOMB")
        self.board.player_piece.origin = Vector2(5, 4)

        self.board.run_powerup(self.board.player_manager.power_up)

        for check_vector in check_vectors:
            self.assertIsNone(self.board.grid[check_vector.x][check_vector.y])

    def test_score_line_clears_full_line(self) -> None:
        x: int
        for x in range(self.board.width):
            self.board.grid[x][19] = Block()

        self.board.score_line()

        for x in range(self.board.width):
            self.assertIsNone(self.board.grid[x][19])

        self.assertTrue(self.board.is_animating)
        self.assertTrue(self.board.is_falling_blocks)
        self.assertEqual(self.board.collapse_height, 19)
        self.assertEqual(self.board.scan_height, 18)

    def test_score_line_no_full_line(self) -> None:
        x: int
        for x in range(self.board.width - 1):
            self.board.grid[x][19] = Block()

        self.board.score_line()

        self.assertFalse(self.board.is_animating)
        self.assertIsNotNone(self.board.grid[0][19])

    def test_apply_block_gravity(self) -> None:
        self.board.grid[5][18] = Block()

        self.board.is_animating = True
        self.board.is_falling_blocks = True
        self.board.collapse_height = 19
        self.board.scan_height = 18

        self.board.apply_block_gravity()

        self.assertIsNone(self.board.grid[5][18])
        self.assertIsInstance(self.board.grid[5][19], Block)
        self.assertTrue(self.board.blocks_fell_in_scan)
        self.assertEqual(self.board.scan_height, 17)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
