import unittest
import sys
import os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from packages.GameManager import GameManager  # nopep8


def run_manual_test():
    being_debugged = 'TERM_PROGRAM' in os.environ.keys()

    mgr = GameManager(being_debugged)
    mgr.start_game()


if __name__ == '__main__':
    if '--manual' in sys.argv:
        run_manual_test()
    else:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
