from packages.Board import Board
from packages.Renderer import Renderer
from packages.Vector2 import Vector2


class GameManager():
    game_state: str
    level: int
    board: Board
    renderer: Renderer

    def __init__(self):
        board_dimensions = Vector2(10,20)
        self.renderer = Renderer(board_dimensions)

    def process_input(self, user_input: str):
        pass

    def save_score(self):
        pass

    def game_loop(self):
        pass

    def pause_game(self):
        pass

    def start_game(self):
        pass
