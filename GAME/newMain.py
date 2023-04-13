import numpy as np
import pygame
import Board
import Shape
from shapely.geometry import Point, Polygon, box, LineString
from shapely.geometry import shape as shapely_shape
import shapely
import math
from pygame.time import Clock
import json


# activate the pygame library .
pygame.init()
#clock = pygame.time.Clock()

MOVEEVENT = pygame.USEREVENT + 1 # this is just defining some event that we can use later (with integer key)
pygame.time.set_timer(MOVEEVENT, 40)

# use the font arial
load_from_file = False
# create a surface object, image is drawn on it.
def run():
    if load_from_file == True:
        # load the polygon dictionary from the file
        with open('polygon.json', 'r') as f:
            poly_dict = f.read()
            Polygon_object = shapely_shape(json.loads(poly_dict))
            Polygon_object = Polygon_object.simplify(tolerance=0.01)
            print('simplified size =', Polygon_object.area)

    else:
        point_list = getPointList()
        print('point_list: ', point_list)
        Polygon_object = Polygon(point_list)

    print(Polygon_object)
    #Polygon_object = shapely.set_precision(geometry = Polygon_object, grid_size = 0.0001)
    print(Polygon_object)
    board = Board.Board()
    shape = Shape.Shape(Polygon_object)
    shape.shrink_or_swell_shapely_polygon()
    board.setShape(shape)

    #show the intial board
    board.setShape(shape)
    board.show()

    status = True
    stop = False
    while status:
        for event in pygame.event.get():
            
            if stop == False:
                if event.type == MOVEEVENT:
                    shape.moveForward(board, 0.01)

                    board.setShape(shape)
                    board.show()
                

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        shape.rotate(board, -3)
                    elif event.key == pygame.K_DOWN:
                        shape.rotate(board, 3)
                    elif event.key == pygame.K_LEFT:
                        shape.moveForward(board, 1)
                    
                    
                    board.setShape(shape)
                    board.show()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    # if I ever use this again just tranlate the mous input keep everything in shape the 1.00 scale. 
                    mousePoint = Point(pygame.mouse.get_pos()[0]/board.SCALE, pygame.mouse.get_pos()[1]/board.SCALE)

                    shape.moveTowardsPoint(board, mousePoint, distance=0.1)
                
                    board.setShape(shape)
                    board.show()
                
                if(board.distance_value < 0.01 and stop == False):
                    print('done')
                    largest_rectangle = shape.getLargeRectangle()
                    #print('largest_rectangle: ', largest_rectangle.exterior.coords)
                    
                    for poly in shape.rectangle_list:
                        if poly.is_valid and isinstance(poly, Polygon):
                            #print(poly)
                            board.showPoly(poly)
                            # load the polygon dictionary from the file         



                        
                    board.showPoly(largest_rectangle)

                    poly_dict = json.dumps(largest_rectangle.__geo_interface__)
                    print('size =', largest_rectangle.area)

                    # write the polygon dictionary to a file
                    with open('polygon.json', 'w') as f:
                        f.write(poly_dict)


                    stop = True

        #I figured out the issue, im doing the difference but that makes multipolygons because they are also on the outside of the squares.
        #Easiest way to fix this is to just make the field a polygon and then take the intersection. 
        
        #then I still do not understand why it doesnt come back to the correct spot but okay. 
        #Okay now I do. I am rotating arround the centroid of the shape. -> issue because then the minus rotation is incorrect. so I should rotate first and then itl work?

        #making it a rectangle was dumb 
            
 
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
            if event.type == pygame.QUIT:
                status = False


def getPointList():
    point1 = Point(0.00000, 0.45000)
    point2 = Point(0.00000, 0.55000)
    point3 = Point(0.05000, 0.55000)
    point4 = Point(0.05000, 0.45000)
    


    point_list = [point1, point2, point3, point4, point1]
    return point_list
    
# deactivates the pygame library
run()


  