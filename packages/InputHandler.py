import keyboard
from typing import Literal, TypeAlias, get_args

Command: TypeAlias = Literal["UP", "DOWN",
                             "LEFT", "RIGHT", "ESCAPE", "DUMP", "TRIGGER_POWERUP", "CLOCKWISE_ROTATION", "COUNTERWISE_ROTATION", "RETURN"] | None
KeyPress: TypeAlias = str | None


class InputHandler:
    responses: list[Command] = list(get_args(Command))

    last_keypress: KeyPress
    bindings: dict[KeyPress, Command]

    def __init__(self, bindings: dict[KeyPress, Command] | None = None) -> None:
        default_bindings: dict[KeyPress, Command] = {
            "w": "UP",
            "d": "RIGHT",
            "a": "LEFT",
            "s": "DOWN",
            "h": "DUMP",
            "p": "TRIGGER_POWERUP",
            "e": "CLOCKWISE_ROTATION",
            "q": "COUNTERWISE_ROTATION",
            "enter": "RETURN",
            "esc": "ESCAPE",
        }

        self.last_keypress = None
        keyboard.on_release(self.on_release)
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

    def on_release(self, event: keyboard.KeyboardEvent):
        self.last_keypress = event.name
