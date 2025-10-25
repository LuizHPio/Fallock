from pynput.keyboard import Listener, Key, KeyCode
from typing import Literal, TypeAlias, get_args

Command: TypeAlias = Literal["UP", "DOWN",
                             "LEFT", "RIGHT", "ESCAPE", "DUMP", "TRIGGER_POWERUP", "CLOCKWISE_ROTATION", "COUNTERWISE_ROTATION"] | None
KeyPress: TypeAlias = Key | KeyCode | None


class InputHandler:
    responses: list[Command] = list(get_args(Command))

    listener: Listener
    last_keypress: KeyPress
    bindings: dict[KeyPress, Command]

    def __init__(self, bindings: dict[KeyPress, Command] | None = None) -> None:
        default_bindings: dict[KeyPress, Command] = {
            KeyCode.from_char("w"): "UP",
            KeyCode.from_char("d"): "RIGHT",
            KeyCode.from_char("a"): "LEFT",
            KeyCode.from_char("s"): "DOWN",
            KeyCode.from_char("h"): "DUMP",
            KeyCode.from_char("p"): "TRIGGER_POWERUP",
            KeyCode.from_char("e"): "CLOCKWISE_ROTATION",
            KeyCode.from_char("q"): "COUNTERWISE_ROTATION",
            Key.esc: "ESCAPE",
        }

        self.last_keypress = None
        self.listener = Listener(on_release=self.on_release)
        self.listener.start()
        self.bindings = default_bindings if bindings == None else bindings

    def get_command(self, peek_key: bool = False) -> Command:
        response = self.get_response()

        if not peek_key:
            self.last_keypress = None

        return response

    def get_response(self) -> Command:

        if self.last_keypress in self.bindings:
            return self.bindings[self.last_keypress]

        return None

    def on_release(self, key: Key | KeyCode | None):
        self.last_keypress = key
