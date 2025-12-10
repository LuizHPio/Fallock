from packages.Board import Board
from packages.Renderer import Renderer
from packages.Vector2 import Vector2
from packages.InputHandler import InputHandler, Command
from packages.Player import Player
import time
import math
import curses


class GameManager():
    game_state: str
    level: int
    board: Board
    renderer: Renderer
    target_tickrate: float
    target_framerate: int
    input_handler: InputHandler
    player_manager: Player
    game_running: bool

    def __init__(self, stdscr: curses.window, debug: bool = False):
        self._board_dimensions = Vector2(12, 20)
        self._debug = debug

        self.input_handler = InputHandler(stdscr)
        self.renderer = Renderer(stdscr, self._board_dimensions, self._debug)
        self.player_manager = Player()
        self.player_manager.load_acummulated_score()
        self.board = Board(self._board_dimensions.x,
                           self._board_dimensions.y, self.player_manager)
        self.target_tickrate = 128
        self.target_framerate = 256
        self.level = 1
        self.game_running = False

    def menu(self, first_start: bool = False):
        if first_start:
            self.renderer.selection = "START_GAME"
            self.renderer.show_startscreen()

        while True:
            self.process_input(self.input_handler.get_command())
            time.sleep(0.05)

    def process_input(self, user_input: Command):
        if self.game_running:
            self.game_inputs(user_input)
            return

        self.menu_inputs(user_input)

    def menu_inputs(self, user_input: Command):
        if user_input == "RETURN":
            if self.renderer.current_menu == "START_SCREEN":
                if self.renderer.selection == "START_GAME":
                    self.board = Board(
                        self.board.width, self.board.height, self.player_manager)
                    self.renderer.current_menu = "GAME_SCREEN"
                    self.renderer.selection = None
                    self.game_loop()
                    return

                if self.renderer.selection == "CHANGE_BINDINGS":
                    self.renderer.current_menu = "BINDINGS_SCREEN"
                    self.renderer.show_bindingscreen()
                    self.renderer.selection = None
                    return

                if self.renderer.selection == "QUIT":
                    exit()
                return

            if self.renderer.current_menu == "END_GAME_SCREEN":
                if user_input == "RETURN":
                    self.renderer.current_menu = "START_SCREEN"
                    self.renderer.selection = None
                    self.menu(True)

            if self.renderer.current_menu == "BINDINGS_SCREEN":
                if user_input == "RETURN":
                    if self.renderer.selection == "RETURN_FROM_BINDINGS":
                        self.player_manager.save_acummulated_score()
                        self.renderer.current_menu = "START_SCREEN"
                        self.renderer.show_startscreen()
                        self.renderer.selection = "START_GAME"
                        return

                    self.renderer.set_bind()

        if user_input == "DOWN":
            self.renderer.change_selection(True)
            return

        if user_input == "UP":
            self.renderer.change_selection(False)
            return

        if user_input == "MOUSE_CLICK":
            try:
                _, x, y, _, _ = curses.getmouse()
                if (self.renderer.handle_mouse_click(x, y)):
                    self.process_input("RETURN")
            except curses.error:
                pass

    def game_inputs(self, user_input: Command):
        movement_commands: list[Command] = [
            "LEFT", "RIGHT", "TRIGGER_POWERUP", "CLOCKWISE_ROTATION", "COUNTERWISE_ROTATION"]

        if user_input in movement_commands:
            self.board.movement(user_input)

        if user_input == "DUMP":
            del self.renderer
            self.renderer.debug_print(self.board)
            exit()

        if user_input == "ESCAPE":
            self.pause_game()

    def game_loop(self):
        self.game_running = True

        logic_timer = time.time_ns()
        render_timer = time.time_ns()

        tickrate_counter = 0
        while self.game_running:
            if self.board.is_animating:
                self.board.physics_logic()
                self.renderer.draw(self.board)
                time.sleep(0.016)
            else:
                if self.elapsed_time(logic_timer) > 1/self.target_tickrate:
                    if self.board.game_over:
                        self.game_running = False
                        break
                    if tickrate_counter == self.difficulty(self.level):
                        self.board.physics_logic()
                        tickrate_counter = 0
                    tickrate_counter += 1
                    logic_timer = time.time_ns()

            self.process_input(self.input_handler.get_command())
            self.renderer.draw(self.board)

            self.wait_framerate(render_timer)
            render_timer = time.time_ns()

        self.renderer.current_menu = "END_GAME_SCREEN"
        self.renderer.selection = None
        self.renderer.show_endscreen(
            self.player_manager.score, self.player_manager.acummulated_score)
        self.player_manager.end_match()
        self.menu()

    def wait_framerate(self, timer: int):
        diff = 1/self.target_framerate - self.elapsed_time(timer)
        if diff > 0:
            time.sleep(diff)

    def pause_game(self):
        pass

    def start_game(self):
        self.game_loop()

    def difficulty(self, level: int) -> int:
        # mathematical function that represnts the number of frames that
        # takes for the block to fall based on the level
        return math.ceil(1.096**(-(level-36))+4.6)

    def elapsed_time(self, timer: int) -> float:
        return time.time_ns()/10**9 - timer/10**9
