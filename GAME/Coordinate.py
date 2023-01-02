class Coordinate:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equalsTo(self, coordinate):
        if self.x == coordinate.x and self.y == coordinate.y:
            return True
        else:
            return False
