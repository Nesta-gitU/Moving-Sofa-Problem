import numpy as np
from math import radians, sin, cos
import math
from Coordinate import Coordinate
import copy
# shape array contains all the "turned on" coordinates for the shape used only the outline I guess the rest is kind of useless
# need to make sure the starting shape connects
class Shape:

    def __init__(self):
        self.coordinateList = list()
        
    # note for later: I stole this code from stackoverflow
    def rotate(self, angle = 10):
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
        new_point = (new_point[0] + center_point[0], new_point[1] + center_point[1])

        # turn the point into a coordinate
        new_coordinate = Coordinate(new_point[0], new_point[1])

        return new_coordinate

    def collisionCheck(self, board, coordinateList):
        for coordinate in coordinateList:
            if coordinate.isOutOfBounds(board):
                return True
        return False

    def traceCollisionCheck(self, board, newCoordinateList):
        # Initialize a flag to indicate whether the line between the points has crossed the boundary
        crossed = False

        for coordinate in newCoordinateList:
            # Iterate through each boundary segment (so board.boundary should be a field containing all the boundaries as [((0,0), (0,1)), ((0,1), (1,1)), ((1,1), (1,0)), ((1,0), (0,0))])
            for boundary_segment in board.boundary:
            # Check if the line between the points intersects the boundary segment
                intersection_point = self.intersection((coordinate.x, coordinate.y), boundary_segment)
                if intersection_point is not None:
                    # The line between the points intersects the boundary segment
                    crossed = True
                    break

        # Print the result
        return crossed
    
        

    def normalize(self, coordinate):
        vector = np.array([coordinate.x, coordinate.y])
        norm_vector = vector / np.abs(np.linalg.norm(vector))

        return Coordinate(norm_vector[0], norm_vector[1])

    # maybe if a collision occurs it should move against the wall, or I should just give the NEAT access to distance parameter 
    def moveHorizontal(self, board, distance = 0.5):
        # I should copy the list first and then only copy over the result if no colision. 
        newCoordinateList = copy.deepcopy(self.coordinateList)

        for coordinate in newCoordinateList:
            coordinate.x = coordinate.x + distance
        
        if not self.collisionCheck(board, newCoordinateList):
            # possibly move the self list to against the barrier idk if thats smart
            self.coordinateList = newCoordinateList
        
        # maybe if a collision occurs it should move against the wall, or I should just give the NEAT access to distance parameter 
    
    def moveVertical(self, board, distance = 0.5):
        # I should copy the list first and then only copy over the result if no colision. 
        newCoordinateList = copy.deepcopy(self.coordinateList)

        for coordinate in newCoordinateList:
            coordinate.y = coordinate.y + distance
        
        if not self.collisionCheck(board, newCoordinateList):
            # possibly move the self list to against the barrier idk if thats smart
            self.coordinateList = newCoordinateList
    
    def moveTowardsCoordinate(self, coordinate, distance = 0.5):
        newCoordinateList = copy.deepcopy(self.coordinateList)
        
        centeredCoordinate = Coordinate(coordinate.x - 200, coordinate.y - 200)

        norm_coordinate = self.normalize(centeredCoordinate)

        coordinateToAdd = Coordinate(norm_coordinate.x * distance, norm_coordinate.y * distance)
        print(norm_coordinate.x, coordinateToAdd.y)

        # those two aditions should just be a function in the coordinate class but aight
        for coordinate in newCoordinateList:
            coordinate.y = coordinate.y + coordinateToAdd.y
            coordinate.x = coordinate.x + coordinateToAdd.x
        
        if not self.traceCollisionCheck(newCoordinateList):
            # possibly move the self list to against the barrier idk if thats smart
            self.coordinateList = newCoordinateList 

    # This function returns the intersection point of two line segments, or None if they do not intersect
    # It uses the formula for the intersection of two lines in the form y = mx + b, where m is the slope and b is the y-intercept
    def intersection(self, segment1, segment2):
        a1, a2 = segment1
        b1, b2 = segment2
        da = a2 - a1
        db = b2 - b1
        dp = a1 - b1
        dap = np.array([-da[1], da[0]])
        denom = np.dot(dap, db)
        if denom == 0:
            return None
        num = np.dot(dap, dp)
        return (num / denom.astype(float)) * db + b1