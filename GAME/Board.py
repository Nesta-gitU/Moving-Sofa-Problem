from shapely.geometry import Point, Polygon

class Board:
  def __init__(self):
    self.h = 0.5
    self.distance_point = Point(3.5, 4)
    self.finish_line = Polygon([((3-0.01), 3.5), ((4-0.01), 3.5), ((4-0.01), 3.6), ((3-0.01), 3.6)])
    self.setBounds()

  def get_distance_value(self, shape) -> int:
    # return the absolute distance from the shape to the finish line. the finish line is boundary4
    distance = shape.polygon.distance(self.distance_point)
    return distance
  
  def is_finished(self, shape):
    if shape.polygon.distance(self.finish_line) < 0.01:
      return True
    return False
        
  def setBounds(self):
    # -1's cause the booard is 4*100 but the last pixel is 399 (fuck past me haha)

    boundary1 = Polygon([(-4, 1), (3-0.01, 1), (3-0.01, 4-0.01), (-4, 4-0.01)]) # botom left square
    boundary2 = Polygon([(-4, 0), (4-0.01, 0), (4-0.01, -4-0.01), (-4, -4-0.01)]) # upper
    boundary3 = Polygon([(4-0.01, 0), (4-0.01, 4-0.01), (8-0.01, 4-0.01), (0, -4-0.01)]) # right most boundary
    boundary4 = Polygon([(3, 4-0.01), (4, 4-0.01), (4, 5-0.01), (3, 5-0.01)]) # bottom small boundary
    #boundary5 = Polygon([(0, 0), (0, 1), (-1, 1), (-1, 0)]) # left small boundary

    self.boundaries = [boundary1, boundary2, boundary3, boundary4]#, boundary5]
    #self.field = Polygon([(-4, 0), (-4, 1), (3-0.01, 1), (3-0.01, 8), (4-0.01, 8), (4-0.01, 0), (-4, 0)])

 
