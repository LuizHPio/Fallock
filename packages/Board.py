from packages.Block import Block
from packages.Piece import Piece
from packages.Vector2 import Vector2


class Board:
    player_piece: Piece
    grid: list[list[Block | None]]
    height: int
    width: int

    def __init__(self, width: int, height: int):
        self.height = height
        self.width = width
        self.grid = []
        self.generate_piece()

        for _ in range(self.width):
            self.grid.append([])

        for column in self.grid:
            for _ in range(self.height):
                column.append(None)

    def has_collided(self, piece: Piece) -> bool:
        for relative_block in piece.blocks_relative_pos:
            block_absolute_pos = piece.getBlockAbsPos(relative_block)

            if block_absolute_pos.y == self.height-1:
                return True
            else:
                target = self.grid[block_absolute_pos.x][block_absolute_pos.y+1]
                if not target == None:
                    return True
        return False

    def generate_piece(self):
        self.player_piece = Piece(Vector2(self.width//2, 0))

    def petrify_piece(self, piece: Piece):

        for relative_block in piece.blocks_relative_pos:
            block_abs_pos = Piece.getBlockAbsPos(piece, relative_block)
            self.grid[block_abs_pos.x][block_abs_pos.y] = Block()

        self.generate_piece()

    def fall(self):
        if self.has_collided(self.player_piece):
            self.petrify_piece(self.player_piece)
            return

        self.player_piece.origin.y += 1

    def score_line(self):
        pass
