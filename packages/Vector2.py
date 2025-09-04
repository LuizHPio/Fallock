class Vector2:
    x:int
    y:int
    def __init__(self, x, y):
            self.x = x
            self.y = y
    
    def add(self, a, b):
        return Vector2(a.x+b.x,a.y+b.y)
    
    def __add__(self, b):
        return self.add(self,b)