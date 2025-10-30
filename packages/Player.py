from packages.PowerUp import PowerUp
from dataclasses import dataclass
from typing import Literal, TypeAlias
import pickle
import os

ScoreActions: TypeAlias = Literal["LINE_CLEAR", "BLOCK_DESTROYED"]
SAVE_FILE_LOCATION = "./data/"
DATA_FILE_NAME = "data.bin"


@dataclass
class DataBlob:
    acummulated_score: int


class Player:
    power_up: PowerUp
    acummulated_score: int
    score: int

    def __init__(self) -> None:
        self.score = 0
        self.power_up = PowerUp(None)
        self.acummulated_score = 0
        self.load_acummulated_score()

    def end_match(self):
        self.acummulated_score += self.score
        self.score = 0
        self.power_up = PowerUp(None)
        self.save_acummulated_score()

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

    def save_acummulated_score(self, save_file_location: str | None = None):
        save_file_to_save: str
        save_file_to_save = (
            SAVE_FILE_LOCATION + DATA_FILE_NAME) if save_file_location == None else save_file_location

        try:
            with open(save_file_to_save, "wb") as file:
                try:
                    data = DataBlob(self.acummulated_score)
                    pickle.dump(data, file)
                except Exception as error:
                    print("Could not save acummulated score")
                    print(error)

        except Exception as error:
            print("Could not save score.")
            print(error)

    def load_acummulated_score(self, save_file_location: str | None = None):
        save_file_to_load: str
        save_file_to_load = (
            SAVE_FILE_LOCATION + DATA_FILE_NAME) if save_file_location == None else save_file_location

        if self.is_file_empty(save_file_to_load) or not os.path.exists(save_file_to_load):
            return

        with open(save_file_to_load, "rb") as file:
            try:
                loaded_blob: DataBlob = pickle.load(file)
                self.acummulated_score = loaded_blob.acummulated_score
            except Exception as error:
                print("Could not load acummulated score")
                print(error)

    @staticmethod
    def is_file_empty(filepath: str):
        if not os.path.exists(filepath):
            print("file not found")
            return False
        return os.path.getsize(filepath) == 0
