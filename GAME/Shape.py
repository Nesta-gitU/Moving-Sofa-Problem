import numpy as np
from math import radians, sin, cos
import math
from Coordinate import Coordinate
# shape array contains all the "turned on" coordinates for the shape used only the outline I guess the rest is kind of useless
# need to make sure the starting shape connects
class Shape:

    def __init__(self):
        self.coordinateList = list()
        
    # note for later: I stole this code from stackoverflow
    def rotate(self, angle):
        """Rotates the given polygon which consists of corners represented as (x,y)
        around center_point (origin by default)
        Rotation is counter-clockwise
        Angle is in degrees
        """

        #get avg of all the points (approximation of the centroid)
        x = [coordinate.x for coordinate in self.coordinateList]
        y = [coordinate.y for coordinate in self.coordinateList]
        
        coordinateAvg = Coordinate(sum(x) / len(self.coordinateList), sum(y) / len(self.coordinateList))

        rotated_polygon = []
        print((angle, (coordinateAvg.x, coordinateAvg.y)))
        for corner in self.coordinateList:
            rotated_corner = self.rotate_point((corner.x, corner.y), angle, (coordinateAvg.x, coordinateAvg.y))
            rotated_polygon.append(rotated_corner)

        self.coordinateList = rotated_polygon

    # note for later: I stole this code from stackoverflow
    def rotate_point(self, point, angle, center_point):
        """Rotates a point around center_point(origin by default)
        Angle is in degrees.
        Rotation is counter-clockwise
        """
        angle_rad = radians(angle % 360)

        # Shift the point so that center_point becomes the origin
        new_point = (point[0] - center_point[0], point[1] - center_point[1])
        new_point = (new_point[0] * cos(angle_rad) - new_point[1] * sin(angle_rad),
                 new_point[0] * sin(angle_rad) + new_point[1] * cos(angle_rad))

        # Reverse the shifting we have done and round to nearest integer
        new_point = (math.ceil(new_point[0] + center_point[0]), math.ceil(new_point[1] + center_point[1]))

        # turn the point into a coordinate
        new_coordinate = Coordinate(new_point[0], new_point[1])

        return new_coordinate
