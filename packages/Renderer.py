from packages.Board import Board
from packages.Vector2 import Vector2
from packages.InputHandler import InputHandler, KeyPress, Command
from typing import Callable, TypeVar, ParamSpec, Literal, TypeAlias, Annotated
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
                                 "BINDINGS_SCREEN", "GAME_SCREEN", "END_GAME_SCREEN"]


UI_Elements: TypeAlias = Literal["START_GAME",
                                 "CHANGE_BINDINGS", "QUIT", "RETURN_FROM_ENDGAME", "RETURN_FROM_BINDINGS", "RESTORE_BINDINGS"] | None

Bounding_boxes: dict[UI_Elements, Annotated[list[Vector2], "length=2"]] = {
    "START_GAME": [Vector2(2, 2), Vector2(22, 8)],
    "CHANGE_BINDINGS": [Vector2(2, 10), Vector2(22, 16)],
    "QUIT": [Vector2(2, 18), Vector2(22, 24)],
    "RETURN_FROM_ENDGAME": [Vector2(0, 0), Vector2(100, 100)],
    "RETURN_FROM_BINDINGS": [Vector2(2, 33), Vector2(24, 39)],
    "RESTORE_BINDINGS": [Vector2(26, 33), Vector2(48, 39)],
}


class Renderer:
    stdscr: curses.window
    board_dimensions: Vector2
    debug: bool
    selection: UI_Elements
    current_menu: MenuScreens
    elements_per_screen: dict[MenuScreens, list[UI_Elements]] = {
        "START_SCREEN": ["START_GAME", "CHANGE_BINDINGS", "QUIT"],
        "BINDINGS_SCREEN": ["RETURN_FROM_BINDINGS", "RESTORE_BINDINGS"],
        "END_GAME_SCREEN": ["RETURN_FROM_ENDGAME"],
    }

    def __init__(self, stdscr: curses.window, board_dimensions: Vector2, debug: bool = False) -> None:
        self._menuRenderers: dict[MenuScreens, Callable[..., None]] = {
            "START_SCREEN": self.show_startscreen,
            "BINDINGS_SCREEN": self.show_bindingscreen
        }

        self.selection = None
        self.debug = debug

        self._generate_dynamic_binding_ui()

        if debug:
            return

        self.board_dimensions = board_dimensions
        self.stdscr = stdscr
        curses.curs_set(0)

        self.require_window_resize()

        self.current_menu = "START_SCREEN"
        self.selection = None

    def _get_key_name(self, key_code: int) -> str:
        special_keys = {
            10: "Enter", 27: "Esc", curses.KEY_ENTER: "Enter",
            curses.KEY_UP: "Cima", curses.KEY_DOWN: "Baixo",
            curses.KEY_LEFT: "Esq", curses.KEY_RIGHT: "Dir",
            ord(' '): "Espaço"
        }
        return special_keys.get(key_code, chr(key_code).upper() if 0 <= key_code < 256 else "?")

    def _generate_dynamic_binding_ui(self):

        grouped_bindings: dict[Command, list[KeyPress]] = {}
        for key, cmd in InputHandler.bindings.items():
            if cmd in grouped_bindings:
                grouped_bindings[cmd].append(key)
            else:
                grouped_bindings[cmd] = []

        start_y = 5
        box_height = 3

        for cmd in grouped_bindings.keys():
            # We have to ignore the type mismatch here because type aliases can't be modified at runtime
            # The code is essentially casting the str as a UI_Element to dynamically create a UI element.
            ui_id: UI_Elements = f"BTN_BIND_{cmd}"  # type: ignore

            self.elements_per_screen["BINDINGS_SCREEN"].append(ui_id)

            top_left = Vector2(2, start_y)
            bottom_right = Vector2(50, start_y + 2)

            # Important note:
            # The following code sets the bounding box that the renderer will \
            # search when the user clicks on the terminal
            # in this specific case the rendering function will use the bounding box to render it aswell
            Bounding_boxes[ui_id] = [top_left, bottom_right]

            start_y += box_height

        self.elements_per_screen["BINDINGS_SCREEN"]

    def require_window_resize(self):

        while (curses.LINES + 1) < self.board_dimensions.x + 20:
            for i in range(2, -1, -1):
                self.show_alert(
                    f"Aumente o terminal verticalmente e aguarde {i} segundos")
                time.sleep(.666)
            curses.update_lines_cols()

        while (curses.COLS + 1) < self.board_dimensions.y + 20:
            for i in range(2, -1, -1):
                self.show_alert(
                    f"Aumente o terminal horizontalmente e aguarde {i} segundos")
                time.sleep(.666)
            curses.update_lines_cols()

    def change_selection(self, forward: bool):
        possible_selections = self.elements_per_screen[self.current_menu]

        if len(possible_selections) <= 1:
            return

        if self.selection is None:
            self.selection = possible_selections[0]
            self._menuRenderers[self.current_menu]()
            return

        current_index = possible_selections.index(self.selection)

        if forward:
            current_index += 1
            if current_index >= len(possible_selections):
                current_index = 0
        else:
            current_index -= 1
            if current_index < 0:
                current_index = len(possible_selections) - 1

        self.selection = possible_selections[current_index]
        self._menuRenderers[self.current_menu]()

    def handle_mouse_click(self, x: int, y: int) -> bool:
        selected = False

        for element_name, (UL, BL) in Bounding_boxes.items():
            if self.is_point_inside_square(Vector2(x, y), UL, BL):

                possible_selections = self.elements_per_screen[self.current_menu]
                if element_name in possible_selections:
                    self.selection = element_name
                    selected = True

        return selected

    @draw_call
    def draw(self, board: Board):
        x_offset = 2
        y_offset = 2

        # draw current level
        self.stdscr.addstr(-2+y_offset, board.width//4 +
                           x_offset, f"Nível atual: {board.level}")

        # draw grid borders
        tlc = Vector2(x_offset-1, y_offset-1)
        rbc = Vector2(board.width+x_offset, board.height+y_offset)

        # draws grid borders
        self.draw_square(tlc, rbc)

        # draw the static blocks
        for x in range(len(board.grid)):
            for y in range(len(board.grid[x])):
                item = board.grid[x][y]
                if item == None:
                    self.stdscr.addstr(y+y_offset, x+x_offset, " ")
                else:
                    self.stdscr.addstr(y+y_offset, x+x_offset, item.symbol)

        # draw piece landing spot
        piece_clone: Piece = board.player_piece.copy()

        # get piece height(distance from origin to bottom), independent of rotation
        biggest_height: int = 0
        for block in piece_clone.blocks_relative_pos:
            if block.y < 0:
                if block.y < biggest_height:
                    biggest_height = block.y

        clone_height: int = abs(biggest_height)

        if piece_clone.origin.y+clone_height < board.height - 1:
            while True:
                piece_clone.origin.y += 1
                if board.has_collided(piece_clone):
                    break

            for block in piece_clone.blocks_relative_pos:
                block_abs = piece_clone.getBlockAbsPos(block)
                self.stdscr.addstr(block_abs.y+y_offset,
                                   block_abs.x+x_offset, "-")

        piece = board.player_piece

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
        self.stdscr.addstr((board.height+2)+3, 2,
                           f"Pontuação acumulada: {board.player_manager.acummulated_score}")

        preview_x = safezone + 6
        preview_start_y = 4

        self.stdscr.addstr(preview_start_y, preview_x-3, "Próximas peças:")

        for i, next_piece in enumerate(board.spawnlist[:3]):

            box_width = 7
            box_height = 4

            box_y = preview_start_y + 2 + i + (i * (box_height + 1))

            tlc_preview = Vector2(preview_x, box_y)
            rbc_preview = Vector2(preview_x + box_width, box_y + box_height)

            sym = None
            if i == 0:
                sym = "$"
            self.draw_square(tlc_preview, rbc_preview, sym)

            center_x = preview_x + (box_width // 2)
            center_y = box_y + (box_height // 2)

            for block in next_piece.blocks_relative_pos:
                draw_x = center_x + block.x
                draw_y = center_y + block.y

                self.stdscr.addstr(draw_y, draw_x, "X")

    @draw_call
    def show_alert(self, message: str):
        self.stdscr.addstr(message)

    @draw_call
    def show_bindingscreen(self, selected_bind: None | Command = None):
        self.stdscr.addstr(2, 2, "CONTROLES (Selecione para alterar)")

        localization = {
            "UP": "Mover Cima", "DOWN": "Mover Baixo",
            "LEFT": "Mover Esq", "RIGHT": "Mover Dir",
            "CLOCKWISE_ROTATION": "Girar Horário",
            "COUNTERWISE_ROTATION": "Girar Anti-H",
            "RETURN": "Selecionar", "ESCAPE": "Sair/Pausar",
            "TRIGGER_POWERUP": "Powerup"
        }

        for ui_element in self.elements_per_screen["BINDINGS_SCREEN"]:
            if ui_element == None:
                continue

            if ui_element == "RETURN_FROM_BINDINGS":
                UL, BR = Bounding_boxes[ui_element]
                is_selected = "+" if self.selection == ui_element else None
                self.draw_square_text(
                    UL, BR, "Voltar", is_selected)
                continue

            if ui_element == "RESTORE_BINDINGS":
                ul, br = Bounding_boxes[ui_element]
                is_selected = "+" if self.selection == ui_element else None
                self.draw_square_text(
                    ul, br, "Restaurar controles", is_selected)
                continue

            if ui_element.startswith("BTN_BIND_"):

                # Another str to Command cast, this one is safe because the ui id was constructed \
                # from a Command literal
                raw_cmd: Command = ui_element.replace(
                    "BTN_BIND_", "")  # type: ignore
                if raw_cmd == None:
                    continue

                keys: list[str] = []
                for key, cmd in InputHandler.bindings.items():
                    if cmd == raw_cmd:
                        if key == None:
                            continue

                        keys.append(self._get_key_name(key))
                keys_str = " / ".join(keys)

                if raw_cmd == selected_bind:
                    display_text = f"{localization.get(raw_cmd, raw_cmd)} : Pressione a tecla nova"
                else:
                    display_text = f"{localization.get(raw_cmd, raw_cmd)} : {keys_str}"

                ul, br = Bounding_boxes[ui_element]

                symbol = "+" if self.selection == ui_element else None

                self.draw_square_text(
                    ul, br, display_text, symbol)

    def set_bind(self):
        if self.selection == None:
            return

        if not self.selection.startswith("BTN_BIND_"):
            return

        cmd: Command = self.selection.replace("BTN_BIND_", "")  # type: ignore

        self.show_bindingscreen(cmd)

        while True:
            try:
                key = self.stdscr.getch()
            except curses.error:
                continue

            if key == curses.ERR:
                continue

            if key == curses.KEY_MOUSE:
                continue

            if key == 27:
                return

            break

        if cmd in InputHandler.bindings.values():
            keys_to_delete: list[KeyPress] = []
            for key_bind, value in InputHandler.bindings.items():
                if value == cmd:
                    keys_to_delete.append(key_bind)

            for key_bind in keys_to_delete:
                del InputHandler.bindings[key_bind]

            InputHandler.bindings[key] = cmd
            self.show_bindingscreen()

    @draw_call
    def show_startscreen(self):

        selected_symbol = "+" if self.selection == "START_GAME" else None
        self.draw_square_text(Vector2(2, 2), Vector2(
            22, 8), "Iniciar Jogo", selected_symbol)

        selected_symbol = "+" if self.selection == "CHANGE_BINDINGS" else None
        self.draw_square_text(
            Vector2(2, 10), Vector2(22, 16), "Mudar controles", selected_symbol)

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
            self.stdscr.addstr(y, left_top_corner.x, draw_with)
            self.stdscr.addstr(y, right_bottom_corner.x, draw_with)

    @draw_call
    def show_endscreen(self, match_score: int, accumulated_score: int):
        self.selection = "RETURN_FROM_ENDGAME"
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

        selected_symbol = "+" if self.selection == "RETURN_FROM_ENDGAME" else None

        self.draw_square_text(top_left, bottom_right, text, selected_symbol)

    def draw_centered_text(self, text_center: Vector2, text: str):
        text_length = len(text)
        start_vector = Vector2(text_center.y, text_center.x-(text_length//2))

        self.stdscr.addstr(start_vector.x, start_vector.y, text)

    def get_square_middle(self, top_left_corner: Vector2, bottom_right_corner: Vector2):
        middle = Vector2((top_left_corner.x+bottom_right_corner.x) //
                         2, (top_left_corner.y+bottom_right_corner.y)//2)
        return middle

    def is_point_inside_square(self, point: Vector2, square_upper_left: Vector2, square_bottom_right: Vector2):
        '''
        Returns true if a point is inside a square defined by upper left and bottom rigth points.

        Note: If the point is exactly on the border of the square the function also returns true.
        '''

        is_betweeen_vertical_axes = False
        if point.x >= square_upper_left.x and point.x <= square_bottom_right.x:
            is_betweeen_vertical_axes = True

        is_between_horizontal_axes = False
        if point.y >= square_upper_left.y and point.y <= square_bottom_right.y:
            is_between_horizontal_axes = True

        return is_between_horizontal_axes and is_betweeen_vertical_axes

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
