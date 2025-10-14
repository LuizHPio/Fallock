import unittest
from unittest.mock import patch, MagicMock, call, PropertyMock
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)


def run_manual_test():
    """
    Runs an interactive, manual test for the Renderer class.
    This requires a terminal and will create a real curses window.
    """
    print("--- Starting Manual Renderer Test ---")
    print("A curses window will open. Press Ctrl+C in this terminal to exit.")
    
    renderer = None 
    try:
        if 'curses' in sys.modules:
            del sys.modules['curses']
        if 'time' in sys.modules:
            del sys.modules['time']
        
        from packages.Renderer import Renderer
        from packages.Vector2 import Vector2
        from packages.Board import Board
        import time

        board_dimensions = Vector2(10, 20)
        board = Board(board_dimensions.x, board_dimensions.y)
        renderer = Renderer(board_dimensions)
        board.generate_piece()

        count = 0
        while True:
            count += 1
            
            if hasattr(board, 'player_piece') and board.player_piece:
                renderer.draw(board.player_piece, board)
            else:
                board.generate_piece()

            if count >= 30:
                count = 0
                if hasattr(board, 'fall'):
                    board.fall()
                else:
                    print("\nError: Board object does not have a 'fall' method. Exiting.")
                    break
            
            time.sleep(1/60) # Simulate a 60 FPS loop

    except KeyboardInterrupt:
        print("\n--- Exiting manual test ---")
    except Exception as e:
        print(f"\nAn error occurred during the manual test: {e}")
    finally:
        if renderer:
            del renderer
        print("Cleanup complete.")



mock_curses = MagicMock()
mock_stdscr = MagicMock()
mock_curses.initscr.return_value = mock_stdscr
module_mocks = {
    'curses': mock_curses,
    'time': MagicMock(),
}

with patch.dict('sys.modules', module_mocks):
    # These imports use the mocked libraries defined above
    from packages.Renderer import Renderer
    from packages.Vector2 import Vector2
    from packages.Board import Board
    from packages.Piece import Piece


class TestRenderer(unittest.TestCase):
    """
    Test suite for the Renderer class.
    Mocks the 'curses' and 'time' libraries to test rendering logic
    without affecting the terminal.
    """

    def setUp(self):
        """
        This method is run before each test.
        It resets the mocks to ensure tests are isolated.
        """
        mock_curses.reset_mock()
        mock_stdscr.reset_mock()

    def test_initialization(self):
        """
        Test that the Renderer initializes curses and the screen correctly.
        """
        mock_curses.LINES = 30
        mock_curses.COLS = 30
        
        board_dims = Vector2(10, 20)
        renderer = Renderer(board_dims)

        mock_curses.initscr.assert_called_once()
        mock_curses.noecho.assert_called_once()
        mock_curses.cbreak.assert_called_once()
        mock_stdscr.keypad.assert_called_once_with(True)
        
        del renderer
        
        mock_curses.nocbreak.assert_called_once()
        mock_stdscr.keypad.assert_called_with(False)
        mock_curses.echo.assert_called_once()
        mock_curses.endwin.assert_called_once()


    def test_require_window_resize_loop(self):
        """
        Test the resize loop by simulating a terminal that is too small initially.
        """
        mock_curses.LINES = 30 
        type(mock_curses).COLS = PropertyMock(side_effect=[5, 30])

        board_dims = Vector2(10, 20)
        _ = Renderer(board_dims)
        
        mock_stdscr.addstr.assert_called_once_with(
            "Aumente o tamanho do terminal horizontalmente e espere 3 segundos..."
        )
        module_mocks['time'].sleep.assert_called_once_with(3)


    def test_draw_logic(self):
        """
        Test the main draw method to ensure it calls stdscr.addstr correctly.
        """
        mock_curses.LINES = 30
        mock_curses.COLS = 30

        board_dims = Vector2(2, 2)
        renderer = Renderer(board_dims)
        board = Board(board_dims.x, board_dims.y)
        board.grid[1][1] = MagicMock(symbol="#")
        piece = Piece(Vector2(0, 0))
        piece.blocks_relative_pos = [Vector2(0, 0)]

        renderer.draw(piece, board)

        mock_stdscr.clear.assert_called_once()
        mock_stdscr.refresh.assert_called_once()

        expected_calls = [
            call(0, 0, "+"), call(0, 3, "+"), call(3, 0, "+"), call(3, 3, "+"),
            call(0, 1, "-"), call(0, 2, "-"), call(3, 1, "-"), call(3, 2, "-"),
            call(1, 0, "|"), call(2, 0, "|"), call(1, 3, "|"), call(2, 3, "|"),
            call(1, 1, " "), call(2, 1, " "), call(1, 2, " "),
            call(2, 2, "#"),
            call(1, 1, "X"),
        ]

        mock_stdscr.addstr.assert_has_calls(expected_calls, any_order=True)
        self.assertEqual(mock_stdscr.addstr.call_count, len(expected_calls))

if __name__ == '__main__':
    if '--manual' in sys.argv:
        run_manual_test()
    else:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)

