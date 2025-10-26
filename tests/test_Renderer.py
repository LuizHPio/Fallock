import unittest
import sys
import os
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from packages.Renderer import Renderer  # nopep8
from packages.Vector2 import Vector2  # nopep8


def run_manual_test():
    being_debugged = 'TERM_PROGRAM' in os.environ.keys()
    if being_debugged != True:
        pass

    renderer = Renderer(board_dimensions=Vector2(5, 5))

    renderer.show_endscreen(0, 0)
    while True:
        time.sleep(0.1)


if __name__ == '__main__':
    if '--manual' in sys.argv:
        run_manual_test()
    else:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
