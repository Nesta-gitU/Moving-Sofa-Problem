import Board
import Shape
from shapely import Polygon, Point
import gymnasium as gym
import numpy as np


class Moving_sofa_env(gym.Env):
    metadata = {"render_modes": []} #only allow not rendering (= None) for optimal cloud compatibility

    def __init__(self) -> None:
        points_list = self.getPointList()
        self.polygon = Polygon(points_list)
        self.shape = Shape.Shape(polygon = self.polygon)
        self.board = Board.Board()
       

        self.render_mode = None

        self.action_space = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90] #, -5, -10, -15, -20, -25]# -30, -35, -40, -45, -50, -55, -60, -65, -70, -75, -80, -85, -90]
        self.state_space = np.arange(self.board.total_boxes) # (x,y) of the boxes that make up the states. FIRST STATE SHOULD BE INITIAL STATE
        
    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        # Reset the board and shape
        self.board = Board.Board()
        self.shape = Shape.Shape(self.polygon)

        # reset should return the initial state and some information
        info = {}
        state = self.board.get_box(self.shape)

        return state, info
    
    def step(self, action):
        previous_distance = self.board.get_distance_value(self.shape)

        # take action
        self.shape.rotate(self.board, degrees = action)
        hit_wall = self.shape.moveForward(self.board, distance = self.board.h)
        
        # check if done
        done = self.board.is_finished(self.shape)

        # get reward
        reward = self.get_reward(previous_distance, hit_wall, done)

         # get info
        info = {}
        
        if done == True:
            return None, reward, done, False, info

        # get state
        state = self.board.get_box(self.shape) # @TODO: check in which state the new shape ends up return that state 

        #print("state: ", state)

        return state, reward, done, False, info
    
    def getPointList(self):
        point = Point(0.1000, 0.5000)
    
        point_list = point.buffer(0.1).exterior.coords
        return point_list
    
    def get_reward(self, previous_distance, hit_wall, done):
        reward = self.board.get_distance_value(self.shape) - previous_distance
        reward = reward * -100
        #if hit_wall == True:
        #    reward += 10
        #if done == True:
        #    reward -= 100

        return reward

