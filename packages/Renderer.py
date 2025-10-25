from packages.Board import Board
from packages.Vector2 import Vector2
from typing import Callable, TypeVar, ParamSpec, Literal, TypeAlias
import curses
import time
import functools
from packages.Piece import Piece
import os

T = TypeVar('T')
P = ParamSpec('P')


def draw_call(func: Callable[P, T]) -> Callable[P, T]:
    """
    A decorator that clears the screen, calls the function,
    and then refreshes the screen.
    """
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        board = None

        if len(args) < 2:
            instance = args[0]
        else:
            instance = args[0]
            board = args[1]

        if isinstance(instance, Renderer):
            # Hack to prevent using the draw functions when debugging
            if instance.debug:
                if isinstance(board, Board):
                    # type: ignore
                    return instance.debug_print(board)  # type: ignore

                def void_return(): return None
                return void_return  # type: ignore

            instance.stdscr.clear()
            result = func(*args, **kwargs)
            instance.stdscr.refresh()
            return result
        else:
            # Fallback if used on a function without 'stdscr'
            return func(*args, **kwargs)

    return wrapper


MenuScreens: TypeAlias = Literal["START_SCREEN",
                                 "GAME_SCREEN", "END_GAME_SCREEN"]

UI_Elements: TypeAlias = Literal["START_GAME",
                                 "CHANGE_BINDINGS", "QUIT", "RETURN_TO_MENU"] | None


class Renderer:
    stdscr: curses.window
    board_dimensions: Vector2
    debug: bool
    selection: UI_Elements
    current_menu: MenuScreens
    elements_per_screen: dict[MenuScreens, list[UI_Elements]] = {
        "START_SCREEN": ["START_GAME", "QUIT"],
    }

    def __init__(self, board_dimensions: Vector2, debug: bool = False) -> None:
        self.selection = None
        self.debug = debug

        if debug:
            return

        self.board_dimensions = board_dimensions
        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.require_window_resize()

        self.current_menu = "START_SCREEN"
        self.selection = None

    def require_window_resize(self):
        while (curses.LINES + 1) < self.board_dimensions.x:
            self.show_alert(
                "Aumente o tamanho do terminal horizontalmente e espere 3 segundos...")
            time.sleep(0.1)

        while (curses.COLS + 1) < self.board_dimensions.y:
            self.show_alert(
                "Aumente o tamanho do terminal horizontalmente e espere 3 segundos...")
            time.sleep(0.1)

    def next_selection(self):
        possible_selections = self.elements_per_screen[self.current_menu]

        if self.selection == None:
            self.selection = possible_selections[0]
            self.show_startscreen()
            return

        current_selection_index = possible_selections.index(self.selection)

        if current_selection_index+2 > len(possible_selections):
            current_selection_index = -1

        self.selection = possible_selections[current_selection_index+1]
        self.show_startscreen()

    def previous_selection(self):

        possible_selections = self.elements_per_screen[self.current_menu]

        if self.selection == None:
            self.selection = possible_selections[0]
            self.show_startscreen()
            return

        current_selection_index = possible_selections.index(self.selection)

        if current_selection_index-1 < 0:
            current_selection_index = len(possible_selections)

        self.selection = possible_selections[current_selection_index-1]
        self.show_startscreen()

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

        # draw current power up
        safezone = board.width+2
        self.stdscr.addstr(
            2, safezone+3, f"Power up atual: {"Nenhum" if board.player_manager.power_up.name == None else board.player_manager.power_up.name}")

        self.stdscr.addstr((board.height+2)+2, 2,
                           f"Pontuação: {board.player_manager.score}")
        self.stdscr.addstr((board.height+2)+3, 2, "Pontuação acumulada: ")

    @draw_call
    def show_alert(self, message: str):
        self.stdscr.addstr(message)

    @draw_call
    def show_bindingscreen(self):
        pass

    @draw_call
    def show_startscreen(self):

        selected_symbol = "+" if self.selection == "START_GAME" else None
        self.draw_square_text(Vector2(2, 2), Vector2(
            22, 8), "Iniciar Jogo", selected_symbol)

        # selected_symbol = "+" if self.selection == "CHANGE_BINDINGS" else None
        # self.draw_square_text(
        #    Vector2(2, 10), Vector2(22, 16), "Mudar controles", selected_symbol)

        selected_symbol = "+" if self.selection == "QUIT" else None
        self.draw_square_text(Vector2(2, 18), Vector2(
            22, 24), "Sair", selected_symbol)

    def draw_square_text(self, left_top_corner: Vector2, right_bottom_corner: Vector2, text: str, symbol: str | None = None):
        self.draw_square(left_top_corner, right_bottom_corner, symbol)
        self.draw_centered_text(self.get_square_middle(
            left_top_corner, right_bottom_corner), text)

    def draw_square(self, left_top_corner: Vector2, right_bottom_corner: Vector2, symbol: str | None = None):
        if left_top_corner.x > right_bottom_corner.x:
            return
        if left_top_corner.y > right_bottom_corner.y:
            return

        self.stdscr.addstr(left_top_corner.y, left_top_corner.x, "+")
        self.stdscr.addstr(left_top_corner.y, right_bottom_corner.x, "+")
        self.stdscr.addstr(right_bottom_corner.y, left_top_corner.x, "+")
        self.stdscr.addstr(right_bottom_corner.y, right_bottom_corner.x, "+")

        if symbol == None:
            draw_with = "-"
        else:
            draw_with = symbol

        for x in range(left_top_corner.x+1, right_bottom_corner.x):
            self.stdscr.addstr(left_top_corner.y, x, draw_with)
            self.stdscr.addstr(right_bottom_corner.y, x, draw_with)

        if symbol == None:
            draw_with = "|"
        else:
            draw_with = symbol

        for y in range(left_top_corner.y+1, right_bottom_corner.y):
            self.stdscr.addstr(y, left_top_corner.x, "|")
            self.stdscr.addstr(y, right_bottom_corner.x, "|")

    @draw_call
    def show_endscreen(self, match_score: int, accumulated_score: int):
        self.selection = "RETURN_TO_MENU"
        screen_height = curses.LINES
        screen_width = curses.COLS

        center_x = screen_width // 2
        top_y = screen_height // 4
        self.draw_centered_text(Vector2(center_x, top_y), "Game Over")

        score_y = top_y + 3
        self.draw_centered_text(Vector2(center_x, score_y),
                                f"Pontuação da Partida: {match_score}")

        accumulated_score_y = top_y + 5
        self.draw_centered_text(Vector2(center_x, accumulated_score_y),
                                f"Pontuação Acumulada: {accumulated_score}")

        button_width = 22
        button_height = 6

        button_bottom_y = screen_height - 3
        button_top_y = button_bottom_y - button_height

        button_left_x = center_x - (button_width // 2)
        button_right_x = center_x + (button_width // 2)

        top_left = Vector2(button_left_x, button_top_y)
        bottom_right = Vector2(button_right_x, button_bottom_y)
        text = "Voltar ao Menu"

        selected_symbol = "+" if self.selection == "RETURN_TO_MENU" else None

        self.draw_square_text(top_left, bottom_right, text, selected_symbol)

    def draw_centered_text(self, text_center: Vector2, text: str):
        text_length = len(text)
        start_vector = Vector2(text_center.y, text_center.x-(text_length//2))

        self.stdscr.addstr(start_vector.x, start_vector.y, text)

    def get_square_middle(self, top_left_corner: Vector2, bottom_right_corner: Vector2):
        middle = Vector2((top_left_corner.x+bottom_right_corner.x) //
                         2, (top_left_corner.y+bottom_right_corner.y)//2)
        return middle

    def __del__(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()

        curses.endwin()

    def debug_print(self, board: Board):
        os.system("clear")
        for y in range(board.height):
            for x in range(board.width):
                for block in board.player_piece.blocks_relative_pos:
                    abs_block = board.player_piece.getBlockAbsPos(block)
                    if abs_block.x == x and abs_block.y == y:
                        print("X", end="")
                        break
                else:
                    if board.grid[x][y] == None:
                        print(" ", end="")
                    else:
                        print("X", end="")
            print("|")
