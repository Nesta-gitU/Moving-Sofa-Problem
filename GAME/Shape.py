import numpy as np
from math import radians, sin, cos
import math
import copy
from shapely.geometry import Point, Polygon, LineString
from shapely.ops import unary_union
from shapely import affinity
from shapely import validation
import shapely
import pygame
from shapely import geometry

# polygon object to represent the shape, this class has some wrappers and additional functionality
class Shape:

    def __init__(self, polygon):
        self.polygon = polygon
        self.collision_bound = None
        self.set_forward_point()

        # for the projection
        self.total_x_movement = 0
        self.total_y_movement = 0
        self.total_rotation = 0
        self.current_rectangle = Polygon([(-4, 0), (-4, 1), (4-0.01, 1), (4-0.01, 0)])
        #self.current_rectangle = shapely.set_precision(geometry = self.current_rectangle, grid_size = 0.0001)
        self.rectangle_list = []
        self.rectangle_list.append(copy.deepcopy(self.current_rectangle))


    
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
    
    def get_boundary_difference(self, board, rectangle):
        final_poly = copy.deepcopy(rectangle)

        final_poly = final_poly.intersection(board.field)

        return final_poly




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

                # compute the needed correction -> max_x > 4-0.01 because we had a collision
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

        if not self.collisionCheck(board, newPolygon):
            self.polygon = newPolygon
            self.forward_point = affinity.translate(self.forward_point, xoff = pointToAdd.x, yoff = pointToAdd.y)
            
            if(self.total_rotation < 90):
            ## for the rectangle projection
                self.total_x_movement += pointToAdd.x
                self.total_y_movement += pointToAdd.y

                # set current rectangle to new translated rectangle and also unrotate it 
                new_rectangle = affinity.translate(self.current_rectangle, xoff = pointToAdd.x, yoff = pointToAdd.y)
                self.current_rectangle = new_rectangle
                boundary_difference = self.get_boundary_difference(board, new_rectangle)
                
                #stop changing this it works perfectly
                if boundary_difference.is_valid and isinstance(boundary_difference, Polygon):
                    board.showPoly(boundary_difference, color = (255,255,255))
                boundary_difference = affinity.rotate(boundary_difference, 360 - self.total_rotation, origin=self.polygon.centroid)
                boundary_difference = affinity.translate(boundary_difference, xoff = -self.total_x_movement, yoff = -self.total_y_movement)
                self.rectangle_list.append(boundary_difference)
                if boundary_difference.is_valid and isinstance(boundary_difference, Polygon):
                    board.showPoly(boundary_difference, color = (255,255,255))
                #print(isinstance(boundary_difference, Polygon))
                #print(shapely.distance(self.polygon, self.current_rectangle.boundary))
            


    
    def rotate(self, board, degrees):
        newPolygon = affinity.rotate(self.polygon, degrees, origin='centroid')

        # in all the situations where a cheat can appear the half way projection is colliding with the boundary
        half_way_projection = affinity.rotate(self.polygon, degrees/2, origin='centroid')

       

        if not self.intersectionCollision(board, newPolygon) and not self.intersectionCollision(board, half_way_projection):
            self.polygon = newPolygon
            # if rotation goes through also rotate the forward point. no collision check needed for the forward point and here also move back
            self.forward_point = affinity.rotate(self.forward_point, degrees, origin=self.polygon.centroid)
            

            if(self.total_rotation < 90):
                ## for the rectangle projection 
                self.total_rotation += degrees
                #self.total_rotation = self.total_rotation % 360

                # set currect rectangle to new rotated rectangle
                new_rectangle = affinity.rotate(self.current_rectangle, degrees, origin=self.polygon.centroid) # copilot making assumptions i didnt even think about yet
                self.current_rectangle = new_rectangle

                # add difference of new rectangle that is straightend (horizontal) and moved back to the rectangle list
                boundary_difference = self.get_boundary_difference(board, new_rectangle)
                boundary_difference = affinity.rotate(boundary_difference, -self.total_rotation, origin=self.polygon.centroid)
                #board.showPoly(boundary_difference)
                boundary_difference = affinity.translate(boundary_difference, xoff = -self.total_x_movement, yoff = -self.total_y_movement)
                if boundary_difference.is_valid and isinstance(boundary_difference, Polygon):
                    board.showPoly(boundary_difference)
                self.rectangle_list.append(boundary_difference)
            

        
        

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

    def shrink_or_swell_shapely_polygon(self, factor=0.10, swell=False):
        ''' returns the shapely polygon which is smaller or bigger by passed factor.
            If swell = True , then it returns bigger polygon, else smaller '''
        

        #my_polygon = mask2poly['geometry'][120]

        shrink_factor = 0.10 #Shrink by 10%
        xs = list(self.polygon.exterior.coords.xy[0])
        ys = list(self.polygon.exterior.coords.xy[1])
        x_center = 0.5 * min(xs) + 0.5 * max(xs)
        y_center = 0.5 * min(ys) + 0.5 * max(ys)
        min_corner = geometry.Point(min(xs), min(ys))
        max_corner = geometry.Point(max(xs), max(ys))
        center = geometry.Point(x_center, y_center)
        shrink_distance = center.distance(min_corner)*0.10

        if swell:
            self.polygon = self.polygon.buffer(shrink_distance) #expand
        else:
            self.polygon = self.polygon.buffer(-shrink_distance) #shrink

        #visualize for debugging
        #x, y = my_polygon.exterior.xy
        #plt.plot(x,y)
        #x, y = my_polygon_shrunken.exterior.xy
        #plt.plot(x,y)
        ## to net let the image be distorted along the axis
        #plt.axis('equal')
        #plt.show()    
    
        #return my_polygon_resized

    ### getter methods

    def getForwardPoint(self) -> Point:
        forward_point = copy.deepcopy(self.forward_point)
        return forward_point

    def getExteriorCoords(self, which = 'polygon') -> list:
        if which == 'polygon':
            polygon = copy.deepcopy(self.polygon)

        if which == 'rectangle':
            polygon = copy.deepcopy(self.current_rectangle)
        return list(polygon.exterior.coords)
    
    def getLargeRectangle(self):
        
        final_poly = self.rectangle_list[0]

        for poly in self.rectangle_list[1:]:
            if poly.is_valid and isinstance(poly, Polygon):
                final_poly = final_poly.intersection(poly)
                #print(final_poly) these are all empty so lets print first 
            

        return final_poly