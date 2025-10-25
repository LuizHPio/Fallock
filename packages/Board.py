from packages.Block import Block
from packages.Piece import Piece, generatableTypes
from packages.Vector2 import Vector2
from packages.InputHandler import Command
from packages.Player import Player
from packages.PowerUp import PowerUp, PowerUpNamesNSpecials
from typing import Callable, Any


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

    def generate_piece(self, type: generatableTypes = None):
        self.player_piece = Piece(Vector2(self.width//2, 0), type)

    def petrify_piece(self, piece: Piece):
        if piece.type == "BOMB":
            if self.player_manager.power_up.name == None:
                return
            self.run_powerup(self.player_manager.power_up)
            self.generate_piece()
            return

        for relative_block in piece.blocks_relative_pos:
            block_abs_pos = Piece.getBlockAbsPos(piece, relative_block)
            self.grid[block_abs_pos.x][block_abs_pos.y] = Block()

        self.generate_piece()

    def piece_can_rotate(self, piece: Piece, is_clock_wise: bool) -> bool:
        new_rel_pos: list[Vector2] = []

        for block in piece.blocks_relative_pos:
            block = piece.vectorRightRotation(block, is_clock_wise)
            new_rel_pos.append(block)

        new_rel_abs_pos: list[Vector2] = []
        for block in new_rel_pos:
            abs_pos = piece.getBlockAbsPos(block)
            new_rel_abs_pos.append(abs_pos)

        for block in new_rel_abs_pos:
            if isinstance(self.grid[block.x][block.y], Block):
                return False

        return True

    def movement(self, command: Command):
        if command == "RIGHT":
            self.player_piece.origin.x += 1
            return

        if command == "LEFT":
            self.player_piece.origin.x -= 1
            return

        if command == "CLOCKWISE_ROTATION":
            is_clockwise = True
            if not self.piece_can_rotate(self.player_piece, is_clockwise):
                return

            self.player_piece.rotateBlocks(is_clockwise)
            return

        if command == "COUNTERWISE_ROTATION":
            is_clockwise = False
            if not self.piece_can_rotate(self.player_piece, is_clockwise):
                return

            self.player_piece.rotateBlocks(is_clockwise)
            return

        if command == "TRIGGER_POWERUP":
            if self.player_manager.power_up.name != None:
                self.run_powerup(self.player_manager.power_up)

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
            self.player_manager.add_score("LINE_CLEAR")

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

    def is_outside_grid(self, vector: Vector2):
        if vector.y > self.height-1 or vector.y < 0:
            return True

        if vector.x > self.width-1 or vector.x < 0:
            return True

        return False

    def run_powerup(self, powerup: PowerUp):

        def teleport_piece():
            for block in self.player_piece.blocks_relative_pos:
                abs_block = self.player_piece.getBlockAbsPos(block)

                for scanning_height in range(self.height-1, -1, -1):
                    current_place = self.grid[abs_block.x][scanning_height]
                    if current_place == None:
                        self.grid[abs_block.x][scanning_height] = Block()
                        break
            self.score_line()

            self.generate_piece()
            powerup.name = None

        def explode_bomb():

            if not powerup.is_active:
                powerup.is_active = True
                self.generate_piece("BOMB")
                return

            # vectors corresponding to the deleted blocks around the bomb, radius = 2

            delete_vectors = [
                Vector2(0, 2),
                Vector2(-1, -1), Vector2(0, -1), Vector2(1, -1),
                Vector2(-2, 0), Vector2(-1, 0), Vector2(1, 0), Vector2(2, 0),
                Vector2(-1, 1), Vector2(0, 1), Vector2(1, 1),
                Vector2(0, -2)]

            bomb_pos = self.player_piece.getBlockAbsPos(
                self.player_piece.blocks_relative_pos[0])

            for delete_vector in delete_vectors:
                abs_delete_pos = bomb_pos + delete_vector
                if self.is_outside_grid(abs_delete_pos):
                    continue

                self.grid[abs_delete_pos.x][abs_delete_pos.y] = None
                self.player_manager.add_score("BLOCK_DESTROYED")

            powerup.name = None
            powerup.is_active = False
            self.generate_piece()

        powerup_functions: dict[PowerUpNamesNSpecials, Callable[..., Any]] = {
            "TELEPORTER": teleport_piece,
            "BOMB": explode_bomb}

        if powerup.name == None:
            return

        powerup_functions[powerup.name]()
