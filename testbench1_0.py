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
		time.sleep(1)

if __name__ == "__main__":
	mainThread()
