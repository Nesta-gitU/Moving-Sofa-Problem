from shapely.geometry import Point, Polygon
import Shape
import numpy as np 
import math

class Board:
  def __init__(self):
    
    self.distance_point = Point(3.5, 4)
    self.finish_line = Polygon([((3-0.01), 3.5), ((4-0.01), 3.5), ((4-0.01), 3.6), ((3-0.01), 3.6)])
    self.setBounds()

    ### box stuff ###
    self.init_boxes()

  def get_distance_value(self, shape) -> int:
    distance = shape.polygon.distance(self.distance_point)

    # Calculate the directional vector between the two points
    direction = (self.distance_point.x - shape.polygon.centroid.x, self.distance_point.y - shape.polygon.centroid.y)

    # Check the sign of the x component of the directional vector
    if direction[1] < 0:
      # If the x component is negative, make the distance negative
      distance = -distance

    # return the absolute distance from the shape to the finish line. the finish line is boundary4
    
    
    return distance
  
  def is_finished(self, shape):
    if self.get_distance_value(shape) < 0.01:
      return True
    return False
        
  def setBounds(self):
    # -1's cause the booard is 4*100 but the last pixel is 399 (fuck past me haha)

    boundary1 = Polygon([(-4, 1), (3-0.01, 1), (3-0.01, 4-0.01), (-4, 4-0.01)]) # botom left square
    boundary2 = Polygon([(-4, 0), (4-0.01, 0), (4-0.01, -4-0.01), (-4, -4-0.01)]) # upper
    boundary3 = Polygon([(4-0.01, 0), (4-0.01, 4-0.01), (8-0.01, 4-0.01), (0, -4-0.01)]) # right most boundary
    #boundary4 = Polygon([(3, 4-0.01), (4, 4-0.01), (4, 5-0.01), (3, 5-0.01)]) # bottom small boundary
    #boundary5 = Polygon([(0, 0), (0, 1), (-1, 1), (-1, 0)]) # left small boundary

    self.boundaries = [boundary1, boundary2, boundary3]# ,boundary4, boundary5]
    self.field = Polygon([(-4, 0), (-4, 1), (3-0.01, 1), (3-0.01, 8), (4-0.01, 8), (4-0.01, 0), (-4, 0)])
    self.horizontal_field = Polygon([(-4, 0), (-4, 1), (4-0.01, 1), (4-0.01, 0)])

  def init_boxes(self):
    self.h = 0.25
    wanted_width = int(1/self.h)
    stack_one_two = int(3/self.h) + int(4/self.h) #section (1) + "rotated" section 2

    self.total_boxes = wanted_width*stack_one_two

    rows = int(4/self.h) 
    columns = int(4/self.h)
    self.boxes = np.reshape(np.arange(rows*columns), (int(4/self.h), int(4/self.h)))

    start_number = self.boxes[wanted_width-1,columns-1] + 1

    for i in range(wanted_width,rows):
      for j in range(columns - wanted_width, columns):
        self.boxes[i, j] = start_number
        start_number += 1
        



  def get_box_index(self, shape: Shape):
    # just give the whole grid. other function ensure we never leave the wanted area anyway 
    x_min, x_max = 0, 4
    y_min, y_max = 0, 4

    i = math.ceil((shape.polygon.centroid.y - y_min) / self.h)
    j = math.ceil((shape.polygon.centroid.x - x_min) / self.h)

    return (i-1, j-1)
  
  def get_box(self, shape :Shape):
    i, j = self.get_box_index(shape)
    return self.boxes[i, j]

