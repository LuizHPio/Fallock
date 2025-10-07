from packages.Board import Board
from packages.Piece import Piece
from packages.Player import Player


class Renderer:
    def __init__(self) -> None:
        pass

    def draw_board(self, board: Board):
        pass

    def draw_piece(self, piece: Piece):
        pass

    def draw_ui(self, player: Player, next_piece: Piece):
        pass

    def refresh_screen(self):
        pass
