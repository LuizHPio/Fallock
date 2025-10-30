from packages.Vector2 import Vector2
import random
from typing import Literal, TypeAlias, Union, get_args

specialTypes: TypeAlias = Literal["BOMB"]
pieceTypes: TypeAlias = Literal["PYRAMID", "LINE", "HALF_SQUARE"]
generatableTypes: TypeAlias = Union[specialTypes, pieceTypes, None]


class Piece:
    type: pieceTypes | specialTypes
    origin: Vector2
    blocks_relative_pos: list[Vector2]
    height: int

    def __init__(self, origin: Vector2, type: generatableTypes = None):

        self.type = Piece.getRandomType() if type == None else type
        self.origin = origin
        self.blocks_relative_pos = []
        self.materializeType(self.type)
        self.height = 0

    def copy(self) -> 'Piece':
        new_piece = Piece(self.origin.copy(), self.type)

        new_piece.blocks_relative_pos = []
        for block in self.blocks_relative_pos:
            new_piece.blocks_relative_pos.append(block.copy())

        return new_piece

    def materializeType(self, type: generatableTypes):
        if type == "BOMB":
            self.blocks_relative_pos = []

            block1 = Vector2(0, 0)

            self.height = 1
            self.blocks_relative_pos.append(block1)
            return

        if type == "HALF_SQUARE":
            block1 = Vector2(-1, 0)
            block2 = Vector2(-1, 1)
            block3 = Vector2(0, 1)
            block4 = Vector2(1, 1)

            self.blocks_relative_pos.append(block1)
            self.blocks_relative_pos.append(block2)
            self.blocks_relative_pos.append(block3)
            self.blocks_relative_pos.append(block4)

            self.height = 2
            return

        if type == "LINE":
            block1 = Vector2(-1, 0)
            block2 = Vector2(0, 0)
            block3 = Vector2(1, 0)
            block4 = Vector2(2, 0)

            self.blocks_relative_pos.append(block1)
            self.blocks_relative_pos.append(block2)
            self.blocks_relative_pos.append(block3)
            self.blocks_relative_pos.append(block4)

            self.height = 1
            return

        if type == "PYRAMID":
            block1 = Vector2(0, 0)
            block2 = Vector2(-1, 1)
            block3 = Vector2(0, 1)
            block4 = Vector2(1, 1)

            self.blocks_relative_pos.append(block1)
            self.blocks_relative_pos.append(block2)
            self.blocks_relative_pos.append(block3)
            self.blocks_relative_pos.append(block4)

            self.height = 2
            return

    def rotateBlocks(self, is_clock_wise: bool):
        new_rel_pos: list[Vector2] = []

        for block in self.blocks_relative_pos:
            block = self.vectorRightRotation(block, is_clock_wise)
            new_rel_pos.append(block)

        self.blocks_relative_pos = new_rel_pos

    def getBlockAbsPos(self, block: Vector2):
        return block+self.origin

    def vectorRightRotation(self, vector_to_rotate: Vector2, is_clock_wise: bool):
        # clockwise_rotation_matrix =
        # [x][0,  1] = [ y]
        # [y][-1, 0]   [-x]
        #
        # counter_clockwise_matrix =
        # [x][0, -1] = [-x]
        # [y][1, 0 ]   [-y]

        if not is_clock_wise:
            return Vector2(vector_to_rotate.y, -vector_to_rotate.x)
        else:
            return Vector2(-vector_to_rotate.y, vector_to_rotate.x)

    @staticmethod
    def getRandomType() -> pieceTypes:
        return random.choice(list(get_args(pieceTypes)))
