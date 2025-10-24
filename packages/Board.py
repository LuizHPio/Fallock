from packages.Block import Block
from packages.Piece import Piece
from packages.Vector2 import Vector2
from packages.InputHandler import Command
from packages.Player import Player


class Board:
    player_piece: Piece
    player_manager: Player
    grid: list[list[Block | None]]
    height: int
    width: int
    collapse_height: int
    scan_height: int
    is_falling_blocks: bool
    is_animating: bool
    blocks_fell_in_scan: bool

    def __init__(self, width: int, height: int, player_manager: Player):
        self.player_manager = player_manager
        self.height = height
        self.width = width
        self.grid = []
        self.is_animating = False
        self.is_falling_blocks = False
        self.blocks_fell_in_scan = False
        self.collapse_height = -1
        self.scan_height = -1
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

    def movement(self, command: Command):
        if command == "RIGHT":
            self.player_piece.origin.x += 1
            return

        if command == "LEFT":
            self.player_piece.origin.x -= 1
            return

        # implement function to prevent piece from moving outside of the board

    def physics_logic(self):
        if self.is_animating:
            if self.is_falling_blocks:
                self.apply_block_gravity()
                return

        if self.has_collided(self.player_piece):
            self.petrify_piece(self.player_piece)
            self.score_line()
            return

        self.player_piece.origin.y += 1

    def score_line(self):
        full_lines: list[int] = []

        for y in range(self.height-1, -1, -1):
            checking_line: list[Block | None] = []

            for x in range(self.width):
                checking_line.append(self.grid[x][y])

            # line isnt full, continue
            if None in checking_line:
                continue

            full_lines.append(y)

        if full_lines:
            for y in full_lines:
                for x in range(self.width):
                    self.grid[x][y] = None
            self.is_animating = True
            self.is_falling_blocks = True
            self.collapse_height = max(full_lines)
            self.scan_height = max(full_lines) - 1
            self.blocks_fell_in_scan = False

    def apply_block_gravity(self):
        # i will first check from the collapse height and upwards(per line) if there is a block with an empty space below
        # if i find a line with an empty space below i will move the blocks which can move, set the blocks_moved variable and then end the frame
        # in the next frame i will do the same until the blocks_moved variable is not set

        if self.scan_height < 0:
            # full scan donew
            if self.blocks_fell_in_scan:
                self.blocks_fell_in_scan = False
                self.scan_height = self.collapse_height - 1
                return

            self.collapse_height = -1
            self.scan_height = -1
            self.is_animating = False
            self.is_falling_blocks = False
            self.score_line()
            return

        for column in range(self.width):
            if self.scan_height == -1 or self.collapse_height == -1:
                return

            if self.grid[column][self.scan_height] == None:
                continue

            # scan_height starts at index 0, sum one for index and one for below space
            if self.scan_height + 1 < self.height:

                matrix_space = self.grid[column][self.scan_height]
                below_matrix_space = self.grid[column][self.scan_height+1]

                if below_matrix_space == None:
                    self.grid[column][self.scan_height +
                                      1] = matrix_space
                    self.grid[column][self.scan_height] = None
                    self.blocks_fell_in_scan = True

        self.scan_height -= 1
