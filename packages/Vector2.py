from dataclasses import dataclass


@dataclass
class Vector2:
    x: int
    y: int

    @staticmethod
    def add(a: 'Vector2', b: 'Vector2'):
        return Vector2(a.x+b.x, a.y+b.y)

    def __add__(self, b: 'Vector2'):
        return self.add(self, b)
