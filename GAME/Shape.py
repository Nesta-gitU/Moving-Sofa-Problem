import numpy as np
from math import radians, sin, cos
import math
import copy
from shapely.geometry import Point, Polygon, LineString
from shapely import affinity
from shapely import validation
import shapely
import pygame

# polygon object to represent the shape, this class has some wrappers and additional functionality
class Shape:

    def __init__(self, polygon):
        self.polygon = polygon
        self.collision_bound = None
        self.set_forward_point()
    
    def collisionCheck(self, board, newPolygon):
        #return False
        #the first boundary is always the polygon the others are lines
    
            #print('overlaps: ', boundary.overlaps(newPolygon))
            #print('touches: ', boundary.touches(newPolygon))
            #print('within: ', newPolygon.within(boundary))
            #print('contains: ', boundary.contains(newPolygon))
            #print('contains: ', newPolygon.contains(boundary))
            #print('crosses: ', boundary.crosses(newPolygon))
            #print('intersects: ', newPolygon.intersects(boundary))
        if(self.intersectionCollision(board, newPolygon)):
            return True
            
        return self.lineCollision(board, newPolygon)
    
    def intersectionCollision(self, board, newPolygon):
        for boundary in board.boundaries:
            if newPolygon.overlaps(boundary) and not newPolygon.touches(boundary):
                self.collision_bound = boundary
                return True 
        return False
        
    def lineCollision(self, board, newPolygon):
        #return False
        newPolygon_coords = list(newPolygon.exterior.coords)

        for i in range(len(self.getExteriorCoords())):
            line = LineString([newPolygon_coords[i], self.getExteriorCoords()[i]])

            for boundary in board.boundaries:
                if line.intersects(boundary) and not line.touches(boundary):
                    self.collision_bound = boundary
                    return True
        return False

    # maybe if a collision occurs it should move against the wall, or I should just give the NEAT access to distance parameter 
    def moveHorizontal(self, board, distance = 0.5):
        
            
        newPolygon = affinity.translate(self.polygon, xoff = distance)
        
        if not self.collisionCheck(board, newPolygon):
            # possibly move the self list to against the barrier idk if thats smart
            self.polygon = newPolygon

        else:
            if distance > 0:
                # get highest x value of the newPolygon
                # bounds returns min x, min y, max x, max y.
                max_x = newPolygon.bounds[2]

                # compute the needed correction (just as a test for now) -> max_x > 4-0.01 because we had a collision
                correction = (4 - 0.01) - max_x

                # correct movement
                self.polygon = affinity.translate(newPolygon, xoff =  correction)

            else:
                # get lowest x value of newPolygon
                # bounds returns min x, min y, max x, max y.
                min_x = newPolygon.bounds[0]
                
                correction = self.collision_bound.bounds[2] - min_x

                # correct movement
                self.polygon = affinity.translate(newPolygon, xoff =  correction)

        # maybe if a collision occurs it should move against the wall, or I should just give the NEAT access to distance parameter 
    
    def moveVertical(self, board, distance = 0.5):
        
        newPoints = []
        for point in self.polygon.exterior.coords:
            newPoint = Point(point[0], point[1] + distance)
            newPoints.append(newPoint)
        
        newPolygon = Polygon(newPoints)
        
        if not self.collisionCheck(board, newPolygon):
            # possibly move the self list to against the barrier idk if thats smart
            self.polygon = newPolygon
        else:
            if distance < 0:
                # bounds returns min x, min y, max x, max y.
                min_y = newPolygon.bounds[1]
                correction = self.collision_bound.bounds[3] - min_y
                self.polygon = affinity.translate(newPolygon, yoff = correction)

            else:
                max_y = newPolygon.bounds[3]
                correction = self.collision_bound.bounds[1] - max_y
                self.polygon = affinity.translate(newPolygon, yoff =  correction)
    
    def moveTowardsPoint(self, board, coordinate, distance = 0.5):
        centeredPoint = Point(coordinate.x - self.polygon.centroid.x, coordinate.y - self.polygon.centroid.y)

        norm_point = self.normalize(centeredPoint)

        pointToAdd = Point(norm_point.x * distance, norm_point.y * distance)
        #print(norm_point.x, norm_point.y)

        newPoints = []
        for point in self.polygon.exterior.coords:
            newPoint = Point(point[0] + pointToAdd.x, point[1] + pointToAdd.y)
            newPoints.append(newPoint)
        
        newPolygon = Polygon(newPoints)

        print(self.collisionCheck(board, newPolygon))

        if not self.collisionCheck(board, newPolygon):
            self.polygon = newPolygon
            self.forward_point = affinity.translate(self.forward_point, xoff = pointToAdd.x, yoff = pointToAdd.y)
    
    def rotate(self, board, degrees):
        newPolygon = affinity.rotate(self.polygon, degrees, origin='centroid')

        # in all the situations where a cheat can appear the half way projection is colliding with the boundary
        half_way_projection = affinity.rotate(self.polygon, degrees/2, origin='centroid')

       

        if not self.intersectionCollision(board, newPolygon) and not self.intersectionCollision(board, half_way_projection):
            self.polygon = newPolygon
            # if rotation goes through also rotate the forward point. no collision check needed for the forward point 
            self.forward_point = affinity.rotate(self.forward_point, degrees, origin=self.polygon.centroid)
        
        

    def normalize(self, coordinate):
        vector = np.array([coordinate.x, coordinate.y])
        norm_vector = vector / np.abs(np.linalg.norm(vector))

        return Point(norm_vector[0], norm_vector[1])

    def set_forward_point(self):
        # which direction is forward changes based on rotation of the object. So this should be a point that is forward of the center. 
        # and moving forward = moving towards this point
        self.forward_point = Point(self.polygon.centroid.x + 1, self.polygon.centroid.y)

    def moveForward(self, board, distance = 0.5):
        if(self.forward_point == None):
            raise Exception("forward point should be set before moving forward")
        self.moveTowardsPoint(board, self.forward_point, distance)

    ### getter methods

    def getForwardPoint(self) -> Point:
        forward_point = copy.deepcopy(self.forward_point)
        return forward_point

    def getExteriorCoords(self) -> list:
        polygon = copy.deepcopy(self.polygon)
        return list(polygon.exterior.coords)
        