from packages.Board import Board
from packages.Renderer import Renderer
from packages.Vector2 import Vector2
from packages.InputHandler import InputHandler, Command
from packages.Player import Player
import os
import time
import math


class GameManager():
    game_state: str
    level: int
    board: Board
    renderer: Renderer
    target_tickrate: float
    target_framerate: int
    input_handler: InputHandler
    player_manager: Player

    def __init__(self, debug: bool = False):
        board_dimensions = Vector2(12, 20)
        self.renderer = Renderer(board_dimensions, debug)
        self.player_manager = Player()
        self.board = Board(board_dimensions.x,
                           board_dimensions.y, self.player_manager)
        self.input_handler = InputHandler()
        self.target_tickrate = 128
        self.target_framerate = 256
        self.level = 1

    def process_input(self, user_input: Command):
        movement_commands = ["LEFT", "RIGHT"]

        if user_input in movement_commands:
            self.board.movement(user_input)

        if user_input == "DUMP":
            del self.renderer
            self.debug_print(self.board)
            exit()

        if user_input == "ESCAPE":
            self.pause_game()

    def debug_print(self, board: Board):
        os.system("clear")
        for y in range(board.height):
            for x in range(board.width):
                for block in self.board.player_piece.blocks_relative_pos:
                    abs_block = self.board.player_piece.getBlockAbsPos(block)
                    if abs_block.x == x and abs_block.y == y:
                        print("X", end="")
                        break
                else:
                    if board.grid[x][y] == None:
                        print(" ", end="")
                    else:
                        print("X", end="")
            print("|")

    def save_score(self):
        pass

    def game_loop(self):
        logic_timer = time.time_ns()
        render_timer = time.time_ns()

        tickrate_counter = 0
        while True:
            if self.board.is_animating:
                self.renderer.draw(self.board)
                self.board.physics_logic()
            else:
                if self.elapsed_time(logic_timer) > 1/self.target_tickrate:
                    if tickrate_counter == self.difficulty(self.level):
                        self.board.physics_logic()
                        tickrate_counter = 0
                    tickrate_counter += 1
                    logic_timer = time.time_ns()

            self.process_input(self.input_handler.get_command())
            self.renderer.draw(self.board)

            self.wait_framerate(render_timer)
            render_timer = time.time_ns()

    def wait_framerate(self, timer: int):
        if 1/self.target_framerate > self.elapsed_time(timer):
            time.sleep(1/self.target_framerate - self.elapsed_time(timer))

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
