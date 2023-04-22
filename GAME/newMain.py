import numpy as np
import pygame
import Board
import Shape
from shapely.geometry import Point, Polygon, box, LineString, MultiPolygon
from shapely.geometry import shape as shapely_shape
import shapely
import math
from pygame.time import Clock
import pickle

############
# nexts steps are dont work on this its great and amazing but your wasting your time. 
# for this to work you need a path finding algorithm anyway so just do that first then do this. 
# remember the faster you do that the faster you can do this.
############ (but actually next step for this is to record the traveld path in a file too such that you can rerun the proposed largest shape and see if it actually fits.
#             probably involves redoing the set timer thing but thats why I should just branch of into simple branch and complicated branch here)

# activate the pygame library .
pygame.init()
#clock = pygame.time.Clock()

MOVEEVENT = pygame.USEREVENT + 1 # this is just defining some event that we can use later (with integer key)
pygame.time.set_timer(MOVEEVENT, 50)

# use the font arial
load_from_file = False
# create a surface object, image is drawn on it.
def run():
    board = Board.Board()
    if load_from_file == True:
        # load the polygon dictionary from the file
        with open('./my_polygon', "rb") as poly_file:
            Polygon_object = pickle.load(poly_file)
            Polygon_object = Polygon_object.simplify(tolerance=0.01)
            print('simplified size =', Polygon_object.area)

    else:
        point_list = getHammersly(board)
        print('point_list: ', point_list)
        Polygon_object = Polygon(point_list)

    #print(Polygon_object)
    #Polygon_object = shapely.set_precision(geometry = Polygon_object, grid_size = 0.0001)
    #print(Polygon_object)
    shape = Shape.Shape(Polygon_object)
    #shape.shrink_or_swell_shapely_polygon(factor = 0.05)

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
                        # to make more projections 
                        for i in range(30):
                            shape.rotate(board, -0.1)
                    elif event.key == pygame.K_DOWN:
                        for i in range(30):
                            shape.rotate(board, 0.1)
                    elif event.key == pygame.K_RIGHT:
                        shape.moveForward(board, 0.1)
                    elif event.key == pygame.K_LEFT:
                        shape.moveForward(board, -0.1)
                    
                    
                    board.setShape(shape)
                    board.show()
                
                if event.type == pygame.MOUSEBUTTONUP:
                    # if I ever use this again just tranlate the mous input keep everything in shape the 1.00 scale. 
                    mousePoint = Point(pygame.mouse.get_pos()[0]/board.SCALE, pygame.mouse.get_pos()[1]/board.SCALE)

                    shape.moveTowardsPoint(board, mousePoint, distance=0.1)
                
                    board.setShape(shape)
                    board.show()
                
                if (board.distance_value < 0.01 and stop == False):
                    print('done')
                    largest_rectangle = shape.getLargeRectangle()
                    #print('largest_rectangle: ', largest_rectangle.exterior.coords)
                    
                    for poly in shape.rectangle_list:
                        if poly.is_valid and isinstance(poly, Polygon):
                            #print(poly)
                            board.showPoly(poly)
                            # load the polygon dictionary from the file         


                    if not isinstance(largest_rectangle, Polygon):
                        print('multipolygon -> size 0')
                        
                    else:
                        board.showPoly(largest_rectangle) # .geoms[0]

                        print('size =', largest_rectangle.area)

                        # write the polygon dictionary to a file
                        # Save polygon to disc
                        with open('./my_polygon', "wb") as poly_file:
                            pickle.dump(largest_rectangle, poly_file, pickle.HIGHEST_PROTOCOL)

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
    point1 = Point(0.00000, 0.55000)
    point2 = Point(0.00000, 0.65000)
    point3 = Point(0.05000, 0.65000)
    point4 = Point(0.05000, 0.55000)
    


    point_list = [point1, point2, point3, point4, point1]
    return point_list

def getHammersly(board):
    
    center0 = Point(2-(2/math.pi), 1)
    center1 = Point(2, 1)
    center2 = Point(2+(2/math.pi), 1) 

    # Create a circle with radius 5 by buffering the center point
    
    circle0 = center0.buffer(1)
    circle1 = center1.buffer(2/math.pi)
    circle2 = center2.buffer(1)

    rectangle = Polygon([(0.36338,1),(3.63662,1),(3.63662,0),(0.36338,0),(0.36338,1)])

    square_left = Polygon([(0.36338,1),(1.36338,1),(1.36338,0),(0.36338,0),(0.36338,1)])
    square_right = Polygon([(2.63662,1),(3.63662,1),(3.63662,0),(2.63662,0),(2.63662,1)])
    sqaure_middle = rectangle.difference(square_left).difference(square_right)

    left = square_left.intersection(circle0)
    middle = sqaure_middle.difference(circle1)
    right = square_right.intersection(circle2)

    multiPoly = MultiPolygon([left, middle, right])

    #board.showPoly(left)
    #board.showPoly(middle)
    #board.showPoly(right)

    hammer = rectangle.intersection(multiPoly)
    print('area of hammersly sofa: ', hammer.area)
    #board.showPoly(hammer)
    
    # Print the quarter circle polygon
    return hammer

    
# deactivates the pygame library
run()


  