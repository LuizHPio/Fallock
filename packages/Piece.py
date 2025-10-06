from packages.Vector2 import Vector2

from typing import List


class Piece:
    type: str
    origin: Vector2
    blocks: List[Vector2]
    height: int
    isFalling: bool

    def __init__(self, type: str, origin: Vector2):
        self.type = type
        self.origin = origin
        self.blocks = []
        self.materializeType(type)
        self.isFalling = True

    def materializeType(self, type: str):
        if type == "pyramid":
            block1 = Vector2(1, 0)
            block2 = Vector2(0, 1)
            block3 = Vector2(1, 1)
            block4 = Vector2(2, 1)

            self.height = 2

            self.blocks.append(block1)
            self.blocks.append(block2)
            self.blocks.append(block3)
            self.blocks.append(block4)

    def getBlockAbsPos(self, block: Vector2):
        return block+self.origin
