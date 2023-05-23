import Board
import Shape
from shapely import Polygon, Point
import gymnasium as gym
import numpy as np
import copy 
import math

class Moving_sofa_env(gym.Env):
    metadata = {"render_modes": []} #only allow not rendering (= None) for optimal cloud compatibility

    def __init__(self) -> None:
        self.board = Board.Board()
        self.buffer = 0.1

        points_list = self.getPointList()
        self.polygon = Polygon(points_list)
        self.shape = Shape.Shape(polygon = self.polygon)

        self.weight1 = 1
        self.render_mode = None
        #                    0   1   2   3    4     5     6    7
        self.action_space = [45, 90, 135, 180, -135, -90, -45, 0] #, -5, -10, -15, -20, -25]# -30, -35, -40, -45, -50, -55, -60, -65, -70, -75, -80, -85, -90]
        self.state_space = np.arange(self.board.total_boxes) # (x,y) of the boxes that make up the states. FIRST STATE SHOULD BE INITIAL STATE
        
    def reset(self, seed=None, options=None, start_point = None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        #reset the action space
        #self.action_space = copy.deepcopy(self.action_space1)

        #if(start_point == None):
        #    #choose a random start point 
        #    new_x = 0.1
        #    new_y = self.np_random.uniform(0+self.buffer, 1-self.buffer)
        #    point = Point(new_x, new_y)
        #    self.polygon = Polygon(self.getPointList(point))

        #else:
        #   self.polygon = Polygon(self.getPointList(start_point))

        self.polygon = Polygon(self.getPointList())
        # Reset the board and shape
        self.shape = Shape.Shape(self.polygon)
        self.board = Board.Board()
       

        # reset should return the initial state and some information
        info = {}
        state = self.board.get_box(self.shape)

        return state, info
    
    def step(self, action):
        previous_distance = self.board.get_distance_value(self.shape)
        #previous_shape = copy.deepcopy(self.shape)

        # take action
        self.shape.rotate(self.board, degrees = action)
        hit_wall = self.shape.moveForward(self.board, distance = self.board.h)
        self.shape.move_to_box_center(self.board)
        
        
        # check if done
        done = self.board.is_finished(self.shape)

        # get reward
        #reward = self.get_reward(previous_distance, hit_wall, done)
        reward = self.get_weighted_reward(previous_distance=previous_distance, hit_wall=hit_wall, done=done)

         # get info
        info = {}
        
        if done == True:
            #reward += 100
            return None, reward, done, False, info
        #if self.shape.polygon.centroid.x > 3:
        #    #print('hello')
        #    self.action_space = copy.deepcopy(self.action_space2)

        # get state
        state = self.board.get_box(self.shape) # @TODO: check in which state the new shape ends up return that state 

        #print("state: ", state)

        return state, reward, done, False, info
    
    def getPointList(self, point = None):

        if point == None:
            point = self.get_middle_box_center()
    
        point_list = point.buffer(self.buffer).exterior.coords
        return point_list
    
    def get_middle_box_center(self) -> Point:
        n_height = 1/self.board.h

        if n_height % 2 == 0: #even
            row_index = n_height/2 + 1 - 1 #-1 cause 0 indexing
        else: #uneven 
            row_index = math.ceil(n_height/2) - 1 #-1 cause 0 index

        col_index = 0 #first column 

        point = self.board.box_centers[int(row_index), col_index]

        return point 



    
    def get_distance_reward(self, previous_distance, hit_wall, done):
        ### note for myself ###
        # distance should decrease with each step, because we move towards a far away point
        # so pervious distance should be larger than current distance
        # which means we define the reward as the ammount we got closer to that point, which is:
        # reward = previous_distance - current_distance
        #######################
        reward = previous_distance - self.board.get_distance_value(self.shape) 
        #print("previous_distance: ", previous_distance)
        #print("current_distance: ", self.board.get_distance_value(self.shape))
        reward = reward * 100
        if hit_wall == True:
            reward -= 10
        #if done == True:
        #    reward -= 100

        return reward

    def get_area_reward(self, previous_shape, hit_wall, action):
        overlap = self.shape.current_rectangle.intersection(previous_shape.current_rectangle)
        reward = self.board.horizontal_field.intersection(self.shape.rectangle_list[-1]).area

        if hit_wall == True:
            reward -= 10
        #print(area)
        return reward
    
    def get_weighted_reward(self, previous_distance, hit_wall, done):
        reward1 =  previous_distance - self.board.get_distance_value(self.shape) 
        if reward1 < 0:
            reward1 = reward1 * 2
        #elif reward1 == 0:
        #    reward1 = -self.board.h

        reward2 = self.board.horizontal_field.intersection(self.shape.rectangle_list[-1]).area
        
        weight2 = 1 - self.weight1
        reward = self.weight1 * reward1 + weight2 * reward2
        if hit_wall == True:
            #reward -= 10
            pass

        return reward