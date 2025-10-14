from packages.Renderer import *
import unittest
import time


class RendererManualTester():
    def test_draw(self):
        board_dimensions = Vector2(10, 20)
        board = Board(board_dimensions.x, board_dimensions.y)
        renderer = Renderer(board_dimensions)
        board.generate_piece()

        count = 0
        while True:
            count += 1
            renderer.draw(board.player_piece, board)
            if count == 30:
                count = 0
                board.fall()
            time.sleep(0.00834)


class RendererTester(unittest.TestCase):
    def func(self):
        pass


if __name__ == "__main__":
    manual = RendererManualTester()
    manual.test_draw()
