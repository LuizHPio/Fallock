from packages.Piece import Piece
from packages.Vector2 import Vector2

from typing import List


class Matrix:
    pieces: List[Piece]
    length: int

    def __init__(self, length: int = 10):
        self.pieces = []
        self.length = length

    def draw(self):
        for y in range(self.length):
            for x in range(self.length):
                # loopar por todos as posições da matriz
                hasPiece = False
                for piece in self.pieces:
                    for block in piece.blocks:
                        if block.x+piece.origin.x == x and block.y+piece.origin.y == y:
                            print("X", end="")
                            hasPiece = True
                if not hasPiece:
                    print(" ", end="")
            # terminar linha
            print("'")

    def fall(self):
        for piece in self.pieces:
            if piece.isFalling:
                if self.hasCollided(piece):
                    piece.isFalling = False
                else:
                    piece.origin.y += 1

    def createPiece(self):
        newPiece = Piece(type="pyramid", origin=Vector2(self.length//2-1, 0))
        self.pieces.append(newPiece)

    def rotatePiece(self, piece: Piece):
        if piece.type == "pyramid":
            pass

    def hasCollided(self, piece: Piece):
        canFall = True
        for block in piece.blocks:
            # loopar pelos blocos no nosso pedaço caindo
            if block.y == piece.height-1:
                # checar se o bloco estiver no fundo do pedaço
                if block.y+1+piece.origin.y == self.length:
                    # checar se colidiu com o solo
                    canFall = False
                    return not canFall

                for staticPiece in self.pieces:
                    if staticPiece.isFalling:
                        continue

                    for staticBlock in staticPiece.blocks:
                        # loopar por todos os blocos que estão no chão
                        staticBlockAbsPos = staticPiece.getBlockAbsPos(
                            staticBlock)
                        blockAbsPos = piece.getBlockAbsPos(block)

                        if (staticBlockAbsPos.x == blockAbsPos.x) and (staticBlockAbsPos.y == blockAbsPos.y+1):
                            # checar se o bloco no chão está embaixo do bloco
                            canFall = False
                            return not canFall
        return not canFall
