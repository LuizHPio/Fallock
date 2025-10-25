from typing import Literal, TypeAlias, Union, get_args
import random

PowerUpNames: TypeAlias = Literal["TELEPORTER", "BOMB"]
PowerUpNamesNNone: TypeAlias = Union[PowerUpNames, None]


class PowerUp():
    name: PowerUpNamesNNone
    is_active: bool

    def __init__(self, power_up: PowerUpNamesNNone = None) -> None:
        self.is_active = False
        self.name = random.choice(
            list(get_args(PowerUpNames))) if power_up == None else power_up

    def activate(self):
        pass

    def deactivate(self):
        pass
