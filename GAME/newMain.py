import numpy as np
import pygame
import Board
import Shape
from shapely.geometry import Point, Polygon, box, LineString
import shapely
import math
from pygame.time import Clock


# activate the pygame library .
pygame.init()
#clock = pygame.time.Clock()

MOVEEVENT = pygame.USEREVENT + 1 # this is just defining some event that we can use later (with integer key)
pygame.time.set_timer(MOVEEVENT, 20)

# use the font arial

# create a surface object, image is drawn on it.
def run():
    point_list = getPointList()
    print('point_list: ', point_list)

    board = Board.Board()
    shape = Shape.Shape(Polygon(point_list))
    board.setShape(shape)

    #show the intial board
    board.setShape(shape)
    board.show()

    status = True
    while status:
        for event in pygame.event.get():
            
            if event.type == MOVEEVENT:
                shape.moveForward(board, 0.01)

                board.setShape(shape)
                board.show()
            

            if event.type == pygame.KEYDOWN:
                print(event.type)
                if event.key == pygame.K_UP:
                    shape.rotate(board, -3)
                elif event.key == pygame.K_DOWN:
                    shape.rotate(board, 3)
                elif event.key == pygame.K_LEFT:
                    shape.moveForward(board, 10)
                
                board.setShape(shape)
                board.show()

            
 
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
            if event.type == pygame.QUIT:
                status = False


def getPointList():
    point1 = Point(0, 0.25)
    point2 = Point(0, 0.75)
    point3 = Point(0.5, 0.75)
    point5 = Point(0.5, 0.25)


    point_list = [point1, point2, point3, point5]
    return point_list
    
# deactivates the pygame library
run()


  