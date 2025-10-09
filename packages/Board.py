from packages.Block import Block
from packages.Piece import Piece


class Board:
    grid: list[list[Block|None]]
    height: int
    width: int

    def __init__(self, height:int, width:int):
        self.height = height
        self.width = width


        for _ in range(self.width):
            self.grid.append([])

        for column in self.grid:
            for _ in range(self.height):
                column.append(None)

    def has_collided(self, piece: Piece) -> bool:
        for piece_block in piece.blocks:
            if piece.getBlockAbsPos(piece_block).y == self.height:
                return True
            else:
                if not self.grid[piece_block.x][piece_block.y+1] == None:
                    return True
        return False

    def score_line(self):
        pass
