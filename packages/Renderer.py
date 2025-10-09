from packages.Board import Board
from packages.Vector2 import Vector2
from typing import Callable, TypeVar, ParamSpec
import curses, time, functools

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

    def __init__(self, board_dimensions: Vector2) -> None:
        
        self.board_dimensions = board_dimensions
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)


    def require_window_resize(self):
        while (curses.LINES + 1) < self.board_dimensions.x:
            self.show_alert("Aumente o tamanho do terminal horizontalmente e espere 3 segundos...")
            time.sleep(3)

        self.require_window_resize()

        while (curses.COLS + 1) < self.board_dimensions.y:
            self.show_alert("Aumente o tamanho do terminal horizontalmente e espere 3 segundos...")
            time.sleep(3)

        self.require_window_resize()
        
    @draw_call
    def draw(self, board: Board):

        #firstly draw the static blocks
        for column in board.grid:
            for item in column:
                if item == None:
                    self.stdscr.addstr(" ")
                else:
                    self.stdscr.addstr(item.symbol)
            self.stdscr.addstr("\n")

    @draw_call
    def show_alert(self, message: str):
        self.stdscr.addstr(message)

    def refresh_screen(self):
        pass

    def __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()

        curses.endwin()
