import Board
import Shape
from Coordinate import Coordinate
from PIL import Image 
import matplotlib.pyplot as plt
from pynput import keyboard
import msvcrt

def main():
    board = Board.Board()
    board.show()

    shape = Shape.Shape()
    setSquare(shape)
    board.setShape(shape)
    board.show()

    shape.rotate(30)
    board.setShape(shape)
    board.show()

    plt.show()


# temporary way to make shapes
def setSquare(shape):

    for x in range(20  ,61):
        for y in range(40,61):
            shape.coordinateList.append(Coordinate(x,y))
        
    

if __name__ == "__main__":
    main()

    