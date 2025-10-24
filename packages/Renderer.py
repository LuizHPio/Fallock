from packages.Board import Board
from packages.Vector2 import Vector2
from typing import Callable, TypeVar, ParamSpec
import curses
import time
import functools
from packages.Piece import Piece

T = TypeVar('T')
P = ParamSpec('P')


def draw_call(func: Callable[P, T]) -> Callable[P, T]:
    """
    A decorator that clears the screen, calls the function,
    and then refreshes the screen.
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        instance = args[0]

        if isinstance(instance, Renderer):
            # Hack to prevent using the draw functions when debugging
            if instance.debug:
                def void_return(): return None
                result: T = void_return  # type: ignore
                return result

            instance.stdscr.clear()
            result = func(*args, **kwargs)
            instance.stdscr.refresh()
            return result
        else:
            # Fallback if used on a function without 'stdscr'
            return func(*args, **kwargs)

    return wrapper


class Renderer:
    stdscr: curses.window
    board_dimensions: Vector2
    debug: bool

    def __init__(self, board_dimensions: Vector2, debug: bool = False) -> None:
        self.debug = debug

        if debug:
            return

        self.board_dimensions = board_dimensions
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.require_window_resize()

    def require_window_resize(self):
        while (curses.LINES + 1) < self.board_dimensions.x:
            self.show_alert(
                "Aumente o tamanho do terminal horizontalmente e espere 3 segundos...")
            time.sleep(3)

        while (curses.COLS + 1) < self.board_dimensions.y:
            self.show_alert(
                "Aumente o tamanho do terminal horizontalmente e espere 3 segundos...")
            time.sleep(3)

    @draw_call
    def draw(self, board: Board):

        piece = board.player_piece

        # draw grid borders

        for x in range(1, board.width+1):  # draw top and bottom limits
            self.stdscr.addstr(0, x, "-")
            self.stdscr.addstr(board.height+1, x, "-")

        for y in range(1, board.height+1):  # draw left and right limits
            self.stdscr.addstr(y, 0, "|")
            self.stdscr.addstr(y, board.width+1, "|")

        # draw corners
        self.stdscr.addstr(0, 0, "+")
        self.stdscr.addstr(0, board.width+1, "+")
        self.stdscr.addstr(board.height+1, 0, "+")
        self.stdscr.addstr(board.height+1, board.width+1, "+")

        # draw the static blocks
        x_offset = 1
        y_offset = 1
        for x in range(len(board.grid)):
            for y in range(len(board.grid[x])):
                item = board.grid[x][y]
                if item == None:
                    self.stdscr.addstr(y+y_offset, x+x_offset, " ")
                else:
                    self.stdscr.addstr(y+y_offset, x+x_offset, item.symbol)

        # draw current piece
        for piece_block in piece.blocks_relative_pos:
            abs_pos = Piece.getBlockAbsPos(piece, piece_block)
            self.stdscr.addstr(abs_pos.y+y_offset, abs_pos.x+x_offset, "X")

    @draw_call
    def show_alert(self, message: str):
        self.stdscr.addstr(message)

    def __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()

        curses.endwin()
