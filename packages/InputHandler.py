import curses
from typing import Literal, TypeAlias, get_args

Command: TypeAlias = Literal["UP", "DOWN",
                             "LEFT", "RIGHT", "ESCAPE", "DUMP", "TRIGGER_POWERUP", "CLOCKWISE_ROTATION", "COUNTERWISE_ROTATION", "RETURN", "MOUSE_CLICK", "MOUSE_MOVEMENT"] | None
KeyPress: TypeAlias = int | None


class InputHandler:
    responses: list[Command] = list(get_args(Command))

    last_keypress: KeyPress
    bindings: dict[KeyPress, Command] = {}

    def __init__(self, stdscr: curses.window, bindings: dict[KeyPress, Command] | None = None) -> None:
        self.default_bindings: dict[KeyPress, Command] = {
            ord("w"): "UP",
            ord("d"): "RIGHT",
            ord("a"): "LEFT",
            ord("s"): "DOWN",
            ord("p"): "TRIGGER_POWERUP",
            ord("e"): "CLOCKWISE_ROTATION",
            ord("q"): "COUNTERWISE_ROTATION",
            curses.KEY_ENTER: "RETURN",
            10: "RETURN",
        }

        self.stdscr = stdscr
        self.stdscr.keypad(True)
        curses.mousemask(curses.ALL_MOUSE_EVENTS |
                         curses.REPORT_MOUSE_POSITION)
        self.stdscr.nodelay(True)
        self.__class__.bindings = self.default_bindings if bindings == None else bindings

    def get_command(self) -> Command:
        try:
            key = self.stdscr.getch()
        except curses.error:
            return None

        if key == curses.ERR:
            return None

        if key == curses.KEY_MOUSE:
            return "MOUSE_CLICK"

        return self.__class__.bindings.get(key, None)

    def restore_bindings(self):
        self.__class__.bindings = self.default_bindings
