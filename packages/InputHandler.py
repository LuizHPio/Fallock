from pynput.keyboard import Listener, Key, KeyCode
from typing import Literal, TypeAlias, get_args

Command: TypeAlias = Literal["UP", "DOWN", "LEFT", "RIGHT"] | None

class InputHandler:
    responses:list[Command] = list(get_args(Command))

    listener: Listener
    last_keypress: Key | KeyCode | None
    bindings: dict[KeyCode, Command]

    def __init__(self, bindings: dict[KeyCode, Command] | None = None) -> None:
        default_bindings: dict[KeyCode, Command] = {
            KeyCode.from_char("w"): "UP",
            KeyCode.from_char("d"): "RIGHT",
            KeyCode.from_char("a"): "LEFT",
            KeyCode.from_char("s"): "DOWN",
        }

        self.last_keypress = None
        self.listener = Listener(on_release=self.on_release)
        self.listener.start()

        if bindings == None:
            self.bindings = default_bindings

            
    def get_command(self, peek_key: bool = False) -> Command:
        response = self.get_response()

        if not peek_key:
            self.last_keypress = None

        return response
    

    def get_response(self) -> Command:

        if self.last_keypress in self.bindings:
            if not isinstance(self.last_keypress, KeyCode):
                return
            
            return self.bindings[self.last_keypress]

        return None
    
    def on_release(self, key: Key | KeyCode | None):
        self.last_keypress = key
