from packages.GameManager import GameManager
import curses


def main(stdscr: curses.window):
    mgr = GameManager(stdscr)
    mgr.menu(True)


if __name__ == "__main__":
    curses.wrapper(main)
