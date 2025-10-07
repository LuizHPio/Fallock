from abc import abstractmethod, ABC


class PowerUp(ABC):
    id: int
    name: str

    def __init__(self) -> None:
        pass

    @abstractmethod
    def activate(self):
        pass
