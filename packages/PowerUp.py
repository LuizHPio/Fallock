from typing import Literal

PowerUpNames = Literal["TELEPORTER", "BOMB"] | None


class PowerUp():
    name: PowerUpNames
    is_active: bool

    def __init__(self) -> None:
        self.is_active = False

    def activate(self):
        pass

    def deactivate(self):
        pass
