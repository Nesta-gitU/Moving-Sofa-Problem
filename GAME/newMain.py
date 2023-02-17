import numpy as np
import pygame
import Board
import Shape
from Coordinate import Coordinate

# activate the pygame library .
pygame.init()
#clock = pygame.time.Clock()
 
# create a surface object, image is drawn on it.
def run():
    board = Board.Board()
    shape = Shape.Shape()

    #create some shape and set in on the board
    setSquare(shape)
    board.setShape(shape)

    #show the intial board
    board.show()
    status = True
    while status:
        for event in pygame.event.get():
            #clock.tick(10)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shape.moveHorizontal(board, -5)
                elif event.key == pygame.K_RIGHT:
                    shape.moveHorizontal(board, 5)
                elif event.key == pygame.K_UP:
                    shape.moveVertical(board, - 5)
                elif event.key == pygame.K_DOWN:
                    shape.moveVertical(board, 5)
                elif event.key == pygame.K_r:
                    shape.rotate()
                
                board.setShape(shape)
                board.show()

            if event.type == pygame.MOUSEBUTTONUP:
                mouseCoordinate = Coordinate(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
                print(mouseCoordinate.x, mouseCoordinate.y)
                shape.moveTowardsCoordinate(mouseCoordinate, distance=10)
                
                board.setShape(shape)
                board.show()

            


            
            
 
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
            if event.type == pygame.QUIT:
                status = False


def setSquare(shape):

    for x in range(20  ,61):
        for y in range(40,61):
            shape.coordinateList.append(Coordinate(x,y))

 
# deactivates the pygame library
run()
