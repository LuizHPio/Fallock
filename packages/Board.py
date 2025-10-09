from packages.Block import Block
from packages.Piece import Piece
from packages.Vector2 import Vector2


class Board:
    player_piece: Piece
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

    def generate_piece(self):
        self.player_piece = Piece(Vector2(self.width//2,0))

    def petrify_piece(self, piece:Piece):
        
        for piece_block in piece.blocks:
            self.grid[piece_block.x][piece_block.y] = Block()

        self.generate_piece()

    def fall(self):
        if self.has_collided(self.player_piece):
            self.petrify_piece(self.player_piece)
            return
        
        self.player_piece.origin.y += 1


    def score_line(self):
        pass
