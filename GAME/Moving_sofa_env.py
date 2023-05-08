import Board
import Shape
from shapely import Polygon, Point
import gymnasium as gym
import numpy as np
import copy 

class Moving_sofa_env(gym.Env):
    metadata = {"render_modes": []} #only allow not rendering (= None) for optimal cloud compatibility

    def __init__(self) -> None:
        point = Point(0.1000, 0.5000)
        self.buffer = 0.1
        points_list = self.getPointList(point)
        self.polygon = Polygon(points_list)
        self.shape = Shape.Shape(polygon = self.polygon)
        self.board = Board.Board()
       

        self.render_mode = None

        self.action_space = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90] #, -45, -50, -55, -60, -65, -70, -75, -80, -85, -90]
        #self.action_space = [-90, -80, -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70, 80, 90] #, -45, -50, -55, -60, -65, -70, -75, -80, -85, -90] 
        # The action space above is a fun example of reward function goes wrong, it has no incentive to actually finish so just goes -90, 90 to optimize reward. 
        # I guess one solution would be two Q-table for section (1) and section (2) of the corridor or we could actually just have two action spaces and that would do the same. Or a time step based negative reward, but that would counter the size optimizater. 
        self.state_space = np.arange(self.board.total_boxes) # (x,y) of the boxes that make up the states. FIRST STATE SHOULD BE INITIAL STATE
        
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        #choose a random start point 
        new_x = 0.1
        new_y = self.np_random.uniform(0+self.buffer, 1-self.buffer)
        point = Point(new_x, new_y)
        self.polygon = Polygon(self.getPointList(point))

        # Reset the board and shape
        self.shape = Shape.Shape(self.polygon)
        self.board = Board.Board()
       

        # reset should return the initial state and some information
        info = {}
        state = self.board.get_box(self.shape)

        return state, info
    
    def step(self, action):
        #previous_distance = self.board.get_distance_value(self.shape)
        previous_shape = copy.deepcopy(self.shape)

        # take action
        self.shape.rotate(self.board, degrees = action)
        hit_wall = self.shape.moveForward(self.board, distance = self.board.h)
        
        # check if done
        done = self.board.is_finished(self.shape)

        # get reward
        #reward = self.get_reward(previous_distance, hit_wall, done)
        reward = self.get_area_reward(previous_shape, hit_wall=hit_wall, action = action)

         # get info
        info = {}
        
        if done == True:
            return None, reward, done, False, info

        # get state
        state = self.board.get_box(self.shape) # @TODO: check in which state the new shape ends up return that state 

        #print("state: ", state)

        return state, reward, done, False, info
    
    def getPointList(self, point):
    
        point_list = point.buffer(self.buffer).exterior.coords
        return point_list
    
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