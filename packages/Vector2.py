from dataclasses import dataclass
import math


@dataclass
class Vector2:
    x: int
    y: int

    def copy(self) -> 'Vector2':
        return Vector2(self.x, self.y)

    def mag(self) -> float:
        ''' returns the magnitude of the vector '''
        return math.sqrt(self.x**2+self.y**2)

    @staticmethod
    def add(a: 'Vector2', b: 'Vector2'):
        return Vector2(a.x+b.x, a.y+b.y)

    def __add__(self, b: 'Vector2'):
        return self.add(self, b)
