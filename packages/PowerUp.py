from typing import Literal, TypeAlias, Union, get_args
import random

PowerUpNames: TypeAlias = Literal["TELEPORTER", "BOMB"]
PowerUpNamesNSpecials: TypeAlias = Union[PowerUpNames, None, Literal["EMPTY"]]


class PowerUp():
    name: PowerUpNamesNSpecials
    is_active: bool

    def __init__(self, power_up: PowerUpNamesNSpecials = "EMPTY") -> None:
        self.is_active = False
        if power_up == "EMPTY":
            self.name = random.choice(list(get_args(PowerUpNames)))
        elif power_up == None:
            self.name = None
        else:
            self.name = power_up

    def activate(self):
        pass

    def deactivate(self):
        pass
