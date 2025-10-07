import curses


class InputHandler:
    def __init__(self) -> None:
        _ = curses.initscr()

    def get_command(self) -> str:
        return ""
