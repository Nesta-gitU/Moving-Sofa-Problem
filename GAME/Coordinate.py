class Coordinate:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equalsTo(self, coordinate):
        if self.x == coordinate.x and self.y == coordinate.y:
            return True
        else:
            return False

    #this should use board such that it is nice and addaptive but for now it doesnt 
    def isOutOfBounds(self, board):
        if self.x < 300:
            if self.y > 100 or self.y < 0 or self.x < 0:
                return True
        else:
            if self.y > 400 or self.y < 0 or self.x > 400:
                return True
        
        return False