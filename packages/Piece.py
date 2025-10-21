from packages.Vector2 import Vector2
import random
from typing import Literal, TypeAlias, get_args

pieceType: TypeAlias = Literal["pyramid"]


class Piece:
    type: pieceType
    origin: Vector2
    blocks_relative_pos: list[Vector2]
    height: int
    isFalling: bool

    def __init__(self, origin: Vector2, type: pieceType | None = None):

        self.type = Piece.getRandomType() if type == None else type
        self.origin = origin
        self.blocks_relative_pos = []
        self.materializeType(self.type)
        self.isFalling = True

    def materializeType(self, type: pieceType):
        if type == "pyramid":
            block1 = Vector2(1, 0)
            block2 = Vector2(0, 1)
            block3 = Vector2(1, 1)
            block4 = Vector2(2, 1)

            self.height = 2

            self.blocks_relative_pos.append(block1)
            self.blocks_relative_pos.append(block2)
            self.blocks_relative_pos.append(block3)
            self.blocks_relative_pos.append(block4)

    def getBlockAbsPos(self, block: Vector2):
        return block+self.origin

    @staticmethod
    def getRandomType() -> pieceType:
        return random.choice(list(get_args(pieceType)))
