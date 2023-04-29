import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt
import pygame
from shapely.geometry import Point, Polygon, box, LineString
from shapely import validation

#Board should only be for display. And to store the boundaries. 
#So like the display in the snake game
class Display_board:
  SCALE = 100
  BOARDSIZE = 10 * SCALE

  def __init__(self):
    #config
    self.font = pygame.font.SysFont('arial', 24)
    self.polygon_color = (0, 0, 255)  # blue
    self.forward_circle_color = (0, 255, 0)  # green
    self.polygon_thickness = 2

    #globals
    self.exterior_coords = []
    self.forward_circle_coords = []
    self.distance_point = Point(3.5, 4)
    self.finish_line = Polygon([((3-0.01), 3.5), ((4-0.01), 3.5), ((4-0.01), 3.6), ((3-0.01), 3.6)])
    self.distance_value = None
  
    # set up the view window
    self.scrn = pygame.display.set_mode((self.BOARDSIZE, self.BOARDSIZE))
    pygame.display.set_caption('Moving Couch')

    self.setBounds()
 
 

  def get_distance_value(self, shape) -> int:
    distance = shape.polygon.distance(self.distance_point)
    return distance


  def show(self):
    # first wipe away the previous shape and reset bounds
    self.scrn.fill((255, 255, 255))
    self.displayBounds()

    # draw the polygon on the screen
    pygame.draw.polygon(self.scrn, self.polygon_color, self.exterior_coords, self.polygon_thickness)

    # draw the forward circle on the screen
    pygame.draw.polygon(self.scrn, self.forward_circle_color, self.forward_circle_coords, width=0)

    # distance_point doesnt move so get coords and draw here
    display_distance_point = Point(self.distance_point.x * self.SCALE, self.distance_point.y * self.SCALE) 
    distance_point_coords = list(display_distance_point.buffer(10).exterior.coords)
    pygame.draw.polygon(self.scrn, (0,0,0), distance_point_coords, width=0)

    # display the value function
    img = self.font.render('Distance = ' + str(self.distance_value), True, (0, 0, 255))
    self.scrn.blit(img, (10, 350))

    #update screen 
    pygame.display.update()
  
  def setShape(self, shape):
    # set the shape for the board
    self.exterior_coords = [(x * self.SCALE, y * self.SCALE) for x, y in shape.getExteriorCoords(which = 'polygon')]

    #self.exterior_coords_rectangle = [(x * self.SCALE, y * self.SCALE) for x, y in shape.getExteriorCoords(which = 'rectangle')]

    # get the forward point for the board
    forward_point = Point(shape.getForwardPoint().x * self.SCALE, shape.getForwardPoint().y * self.SCALE) 

    # set the forward circle for the board
    self.forward_circle_coords = list(forward_point.buffer(10).exterior.coords)

    # set the value 
    self.distance_value = self.get_distance_value(shape)

  def showPoly(self, poly, color = (200,30,40)):
    # show the polygon on the screen
    poly = [(x * self.SCALE, y * self.SCALE) for x, y in poly.exterior.coords]
    pygame.draw.polygon(self.scrn, color, poly, self.polygon_thickness)
    pygame.display.update()

  def displayBounds(self):
    # -1's cause the booard is 4*100 but the last pixel is 399 (fuck past me haha)

    display_boundary1 = Polygon([(0, 1*self.SCALE), (3*self.SCALE-1, 1*self.SCALE), (3*self.SCALE-1, 4*self.SCALE-1), (0, 4*self.SCALE-1)]) 
    display_boundary2 = Polygon([(0, 0), (4*self.SCALE-1, 0), (4*self.SCALE-1, -4*self.SCALE-1), (0, -4*self.SCALE-1)])
    display_boundary3 = Polygon([(4*self.SCALE-1, 0), (4*self.SCALE-1, 4*self.SCALE-1), (8*self.SCALE-1, 4*self.SCALE-1), (8*self.SCALE-1, 0)])
    display_boundary4 = Polygon([(3*self.SCALE, 4*self.SCALE-1), (4*self.SCALE, 4*self.SCALE-1), (4*self.SCALE, 5*self.SCALE-1), (3*self.SCALE, 5*self.SCALE-1),])
    display_boundary5 = Polygon([(0, 0), (0, 1*self.SCALE), (-1*self.SCALE, 1*self.SCALE), (-1*self.SCALE, 0)])

    pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary1.exterior.coords, self.polygon_thickness)
    pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary2.exterior.coords, self.polygon_thickness)
    pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary3.exterior.coords, self.polygon_thickness)
    #pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary4.exterior.coords, self.polygon_thickness)
    #pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary5.exterior.coords, self.polygon_thickness)

    display_finish_line = Polygon([((3-.01)*self.SCALE, 3.5*self.SCALE), ((4-0.01)*self.SCALE, 3.5*self.SCALE), ((4-0.01)*self.SCALE, 3.6*self.SCALE), ((3-0.01)*self.SCALE, 3.6*self.SCALE)])
    pygame.draw.polygon(self.scrn, (0, 0, 0), display_finish_line.exterior.coords, 0)

    #display_field = Polygon([(-4*self.SCALE, 0), (-4*self.SCALE, 1*self.SCALE), ((3-0.01)*self.SCALE, 1*self.SCALE), ((3-0.01)*self.SCALE, 8*self.SCALE), ((4-0.01)*self.SCALE, 8*self.SCALE), ((4-0.01)*self.SCALE, 0), (-4*self.SCALE, 0)])
    #pygame.draw.polygon(self.scrn, (100, 55, 28), display_field.exterior.coords, 1)

    

  def setBounds(self):
    # -1's cause the booard is 4*100 but the last pixel is 399 (fuck past me haha)

    boundary1 = Polygon([(-4, 1), (3-0.01, 1), (3-0.01, 4-0.01), (-4, 4-0.01)]) # botom left square
    boundary2 = Polygon([(-4, 0), (4-0.01, 0), (4-0.01, -4-0.01), (-4, -4-0.01)]) # upper
    boundary3 = Polygon([(4-0.01, 0), (4-0.01, 4-0.01), (8-0.01, 4-0.01), (0, -4-0.01)]) # right most boundary
    boundary4 = Polygon([(3, 4-0.01), (4, 4-0.01), (4, 5-0.01), (3, 5-0.01)]) # bottom small boundary
    #boundary5 = Polygon([(0, 0), (0, 1), (-1, 1), (-1, 0)]) # left small boundary

    self.boundaries = [boundary1, boundary2, boundary3, boundary4]#, boundary5]
    #self.field = Polygon([(-4, 0), (-4, 1), (3-0.01, 1), (3-0.01, 8), (4-0.01, 8), (4-0.01, 0), (-4, 0)])


 
