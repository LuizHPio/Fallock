from packages.Matrix import Matrix
from packages.Piece import Piece
import time, os

def mainThread():
	startMatrix = Matrix()

	startMatrix.createPiece()
	os.system("clear")
	startMatrix.draw()
	time.sleep(1)

	while True:
		os.system("clear")
		startMatrix.draw()
		startMatrix.fall()
		if not isPieceFalling(startMatrix):
			startMatrix.createPiece()

def isPieceFalling(matrix:Matrix) -> bool:
	for piece in matrix.pieces:
		if piece.isFalling:
			return True
	return False

if __name__ == "__main__":
	mainThread()
