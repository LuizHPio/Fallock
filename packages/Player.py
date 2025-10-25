from packages.PowerUp import PowerUp
from typing import Literal, TypeAlias

ScoreActions: TypeAlias = Literal["LINE_CLEAR", "BLOCK_DESTROYED"]


class Player:
    power_up: PowerUp
    acummulated_score: int
    score: int

    def __init__(self) -> None:
        self.score = 0
        self.power_up = PowerUp(None)

    def add_score(self, action: ScoreActions):
        if action == "BLOCK_DESTROYED":
            self.score += 10
            return
        if action == "LINE_CLEAR":
            self.score += 100
            self.add_powerup()
            return

    def add_powerup(self):
        if self.power_up.name != None:
            return
        self.power_up = PowerUp()

    def load_acummulated_score(self):
        pass
