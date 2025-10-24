import unittest
from packages.Board import Board
from packages.Block import Block
from packages.Vector2 import Vector2
from packages.Piece import Piece
from packages.Player import Player


class TestBoard(unittest.TestCase):

    def setUp(self) -> None:
        """Set up a new board instance for each test."""
        self.player_manager: Player = Player()
        self.board: Board = Board(
            width=9, height=20, player_manager=self.player_manager)

    def test_initialization(self) -> None:
        """Test that the board is initialized correctly."""
        self.assertEqual(self.board.width, 9)
        self.assertEqual(self.board.height, 20)
        self.assertEqual(len(self.board.grid), 9)
        self.assertEqual(len(self.board.grid[0]), 20)
        self.assertIsNone(self.board.grid[0][0])
        self.assertIsNotNone(self.board.player_piece)
        self.assertEqual(self.board.player_piece.origin, Vector2(4, 0))
        self.assertFalse(self.board.is_animating)

    def test_has_collided_with_floor(self) -> None:
        """Test piece collision with the bottom of the board."""
        # A piece with any block at y=19 (height-1) should collide.
        self.board.player_piece.origin = Vector2(
            5, 18)  # The bottom part of the T is at y=19
        self.assertTrue(self.board.has_collided(self.board.player_piece))

    def test_has_collided_with_block(self) -> None:
        """Test piece collision with another block on the grid."""
        self.board.grid[5][10] = Block()
        # The bottom part of the T will be at y=9
        self.board.player_piece.origin = Vector2(5, 8)
        self.assertTrue(self.board.has_collided(self.board.player_piece))

    def test_no_collision(self) -> None:
        """Test that no collision is detected when space is free."""
        self.board.player_piece.origin = Vector2(5, 5)
        self.assertFalse(self.board.has_collided(self.board.player_piece))

    def test_block_collapse(self) -> None:
        """Test that blocks with cascade above a cleared line"""

        for i in range(2):
            self.board.player_piece.origin = Vector2(i*3, 18)
            self.board.physics_logic()

        self.board.player_piece.origin = Vector2(0, 16)
        self.board.physics_logic()

        self.board.player_piece.origin = Vector2(6, 18)
        self.board.physics_logic()

        self.board.score_line()
        for _ in range(10):
            self.board.physics_logic()

        self.assertIsInstance(self.board.grid[4][19], Block)

    def test_petrify_piece(self) -> None:
        """Test that a piece's blocks are correctly placed onto the grid."""
        piece_to_petrify: Piece = self.board.player_piece
        piece_to_petrify.origin = Vector2(5, 10)

        self.board.petrify_piece(piece_to_petrify)

        # Check if the T-shape is now in the grid
        self.assertIsInstance(self.board.grid[6][10], Block)  # origin
        self.assertIsInstance(self.board.grid[5][11], Block)  # left part
        self.assertIsInstance(self.board.grid[7][11], Block)  # right part
        self.assertIsInstance(self.board.grid[6][11], Block)  # bottom part

        # Check that a new piece was generated
        self.assertNotEqual(self.board.player_piece, piece_to_petrify)
        self.assertEqual(self.board.player_piece.origin, Vector2(4, 0))

    def test_movement(self) -> None:
        """Test left and right movement."""
        initial_x: int = self.board.player_piece.origin.x

        self.board.movement("RIGHT")
        self.assertEqual(self.board.player_piece.origin.x, initial_x + 1)

        self.board.movement("LEFT")
        self.assertEqual(self.board.player_piece.origin.x, initial_x)

    def test_physics_logic_gravity(self) -> None:
        """Test that piece falls when there's no collision."""
        initial_y: int = self.board.player_piece.origin.y
        self.board.physics_logic()
        self.assertEqual(self.board.player_piece.origin.y, initial_y + 1)

    def test_physics_logic_collision(self) -> None:
        """Test that piece is petrified on collision."""
        self.board.player_piece.origin = Vector2(
            5, 18)  # Set piece to collide on next step
        self.board.physics_logic()
        # Check if the piece was petrified at y=18,19 and a new piece was created at y=0
        self.assertIsInstance(self.board.grid[6][18], Block)
        self.assertIsInstance(self.board.grid[6][19], Block)
        self.assertEqual(self.board.player_piece.origin.y, 0)

    def test_score_line_clears_full_line(self) -> None:
        """Test that a full line is identified and cleared."""
        # Create a full line at the bottom
        x: int
        for x in range(self.board.width):
            self.board.grid[x][19] = Block()

        self.board.score_line()

        # Check that the line is cleared
        for x in range(self.board.width):
            self.assertIsNone(self.board.grid[x][19])

        # Check that animation state is triggered
        self.assertTrue(self.board.is_animating)
        self.assertTrue(self.board.is_falling_blocks)
        self.assertEqual(self.board.collapse_height, 19)
        self.assertEqual(self.board.scan_height, 19)

    def test_score_line_no_full_line(self) -> None:
        """Test that nothing happens if no lines are full."""
        # Create an almost full line
        x: int
        for x in range(self.board.width - 1):
            self.board.grid[x][19] = Block()

        self.board.score_line()

        self.assertFalse(self.board.is_animating)
        self.assertIsNotNone(self.board.grid[0][19])

    def test_apply_block_gravity(self) -> None:
        """Test that blocks fall correctly after a line clear."""
        # Place a block above a cleared line
        self.board.grid[5][18] = Block()

        # Manually set the state as if a line was just cleared at y=19
        self.board.is_animating = True
        self.board.is_falling_blocks = True
        self.board.collapse_height = 19
        self.board.scan_height = 18  # Scan the line with the block

        self.board.apply_block_gravity()

        # The block should have fallen one step
        self.assertIsNone(self.board.grid[5][18])
        self.assertIsInstance(self.board.grid[5][19], Block)
        self.assertTrue(self.board.blocks_fell_in_scan)
        self.assertEqual(self.board.scan_height, 17)  # Scan height moved up


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
