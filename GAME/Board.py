import numpy as np
from PIL import Image 
import matplotlib.pyplot as plt
import pygame
from shapely.geometry import Point, Polygon, box, LineString
from shapely import validation

#Board should only be for display. And to store the boundaries. 
#So like the display in the snake game
class Board:
  SCALE = 100
  BOARDSIZE = 10 * SCALE

  def __init__(self):
    self.polygon_color = (0, 0, 255)  # blue
    self.forward_circle_color = (0, 255, 0)  # green
    self.polygon_thickness = 2
    self.exterior_coords = []
    self.forward_circle_coords = []
    self.value = None

    self.font = pygame.font.SysFont('arial', 24)

  
    # set up the view window
    self.scrn = pygame.display.set_mode((self.BOARDSIZE, self.BOARDSIZE))

    # sceen is needed to set bounds
    self.setBounds()
 
    # set the pygame window name
    pygame.display.set_caption('Moving Couch')

  def get_distance_value(self, shape) -> int:
    # return the absolute distance from the shape to the finish line. the finish line is boundary4
    distance = shape.polygon.distance(self.boundaries[3])
    return distance


  def show(self):
    
    #update the array before showing
    #self.update()
    
    # show updated image
    # Create a Pygame surface from the NumPy array
    # set the polygon color and thickness
    # dont need to redraw the boundaries since they are static
  
    # draw the polygon on the screen
    pygame.draw.polygon(self.scrn, self.polygon_color, self.exterior_coords, self.polygon_thickness)

    pygame.draw.polygon(self.scrn, self.polygon_color, self.exterior_coords_rectangle, self.polygon_thickness)

    # draw the forward circle on the screen
    pygame.draw.polygon(self.scrn, self.forward_circle_color, self.forward_circle_coords, self.polygon_thickness)

    # display the value function
    img = self.font.render('Distance = ' + str(self.distance_value), True, (0, 0, 255))
    self.scrn.blit(img, (10, 350))


 
    # paint screen one time
    pygame.display.update()

    #print the array
    #print(self.grid) 
  
  #this is just the function that sets the things we display above so maybe different name should be better
  def setShape(self, shape):
    # first wipe away the previous shape and reset bounds
    self.scrn.fill((255, 255, 255))
    self.setBounds()

    # set the shape for the board
    self.exterior_coords = [(x * self.SCALE, y * self.SCALE) for x, y in shape.getExteriorCoords(which = 'polygon')]

    self.exterior_coords_rectangle = [(x * self.SCALE, y * self.SCALE) for x, y in shape.getExteriorCoords(which = 'rectangle')]

    # get the forward point for the board
    forward_point = Point(shape.getForwardPoint().x * self.SCALE, shape.getForwardPoint().y * self.SCALE) 

    # set the forward circle for the board
    self.forward_circle_coords = list(forward_point.buffer(10).exterior.coords)

    # set the value 
    self.distance_value = self.get_distance_value(shape)

    #print('shape points list:', shape.getExteriorCoords())
    #print(validation.explain_validity(shape.polygon))

  def showPoly(self, poly, color = (200,30,40)):
    # show the polygon on the screen
    poly = [(x * self.SCALE, y * self.SCALE) for x, y in poly.exterior.coords]
    pygame.draw.polygon(self.scrn, color, poly, self.polygon_thickness)
    pygame.display.update()
    


    


  def setBounds(self):
    # -1's cause the booard is 4*100 but the last pixel is 399 (fuck past me haha)

    #the boundaries have different types but they should all have the .intersects method
    boundary1 = Polygon([(-4, 1), (3-0.01, 1), (3-0.01, 4-0.01), (-4, 4-0.01)]) # botom left square
    boundary2 = Polygon([(-4, 0), (4-0.01, 0), (4-0.01, -4-0.01), (-4, -4-0.01)]) # upper
    boundary3 = Polygon([(4-0.01, 0), (4-0.01, 4-0.01), (8-0.01, 4-0.01), (0, -4-0.01)]) # right most boundary
    
    boundary4 = Polygon([(3, 4-0.01), (4, 4-0.01), (4, 5-0.01), (3, 5-0.01)]) # bottom small boundary
    #boundary5 = Polygon([(0, 0), (0, 1), (-1, 1), (-1, 0)]) # left small boundary

    display_boundary1 = Polygon([(0, 1*self.SCALE), (3*self.SCALE-1, 1*self.SCALE), (3*self.SCALE-1, 4*self.SCALE-1), (0, 4*self.SCALE-1)]) # this returns a polygon object
    display_boundary2 = Polygon([(0, 0), (4*self.SCALE-1, 0), (4*self.SCALE-1, -4*self.SCALE-1), (0, -4*self.SCALE-1)])
    display_boundary3 = Polygon([(4*self.SCALE-1, 0), (4*self.SCALE-1, 4*self.SCALE-1), (8*self.SCALE-1, 4*self.SCALE-1), (8*self.SCALE-1, 0)])
    display_boundary4 = Polygon([(3*self.SCALE, 4*self.SCALE-1), (4*self.SCALE, 4*self.SCALE-1), (4*self.SCALE, 5*self.SCALE-1), (3*self.SCALE, 5*self.SCALE-1),])
    display_boundary5 = Polygon([(0, 0), (0, 1*self.SCALE), (-1*self.SCALE, 1*self.SCALE), (-1*self.SCALE, 0)])
    
 
    self.boundaries = [boundary1, boundary2, boundary3, boundary4]#, boundary5]
    self.field = Polygon([(-4, 0), (-4, 1), (3-0.01, 1), (3-0.01, 8), (4-0.01, 8), (4-0.01, 0), (-4, 0)])

    display_field = Polygon([(-4*self.SCALE, 0), (-4*self.SCALE, 1*self.SCALE), ((3-0.01)*self.SCALE, 1*self.SCALE), ((3-0.01)*self.SCALE, 8*self.SCALE), ((4-0.01)*self.SCALE, 8*self.SCALE), ((4-0.01)*self.SCALE, 0), (-4*self.SCALE, 0)])

    # This is ugly but fine since we will never have more than these 5 boundaries
    pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary1.exterior.coords, self.polygon_thickness)
    pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary2.exterior.coords, self.polygon_thickness)
    pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary3.exterior.coords, self.polygon_thickness)
    pygame.draw.polygon(self.scrn, (150, 0, 0), display_boundary4.exterior.coords, self.polygon_thickness)
    pygame.draw.polygon(self.scrn, (255, 0, 0), display_boundary5.exterior.coords, self.polygon_thickness)

    pygame.draw.polygon(self.scrn, (100, 55, 28), display_field.exterior.coords, 1)

 
