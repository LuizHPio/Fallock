from dataclasses import dataclass


@dataclass
class Vector2:
    x: int
    y: int

    def copy(self) -> 'Vector2':
        return Vector2(self.x, self.y)

    @staticmethod
    def add(a: 'Vector2', b: 'Vector2'):
        return Vector2(a.x+b.x, a.y+b.y)

    def __add__(self, b: 'Vector2'):
        return self.add(self, b)
