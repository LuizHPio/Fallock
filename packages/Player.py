from packages.PowerUp import PowerUp
from typing import Literal, TypeAlias

ScoreActions: TypeAlias = Literal["LINE_CLEAR"]


class Player:
    power_up: PowerUp | None
    acummulated_score: int
    score: int

    def __init__(self) -> None:
        self.score = 0
        self.power_up = None

    def add_score(self, action: ScoreActions):
        if action == "LINE_CLEAR":
            self.score += 100
            self.power_up = PowerUp()

    def add_powerup(self):
        pass

    def load_acummulated_score(self):
        pass
