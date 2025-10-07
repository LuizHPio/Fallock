from packages.Block import Block
from packages.Piece import Piece


class Board:
    grid: list[list[Block]]
    height: int
    width: int

    def __init__(self):
        pass

    def has_collided(self, piece: Piece) -> bool:
        return True

    def petrify_piece(self, piece: Piece):
        pass

    def score_line(self):
        pass
